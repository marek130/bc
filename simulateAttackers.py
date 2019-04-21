from __future__ import division
from functools import reduce
import sys
import json
import re
import time
import random
from bintrees import FastRBTree
from calendar import timegm
from snakes.nets import *


def checkMandatoryFieldsInJSON(json_data):
    return False if ("Source" not in json_data) \
                 or ("IP4" not in json_data['Source'][0]) \
                 or (len(json_data['Source'][0]['IP4']) < 1) \
                 or ("Target" not in json_data) \
                 or ("Port" not in json_data['Target'][0]) \
                 else True


def parseLineOfJSON(line):
    json_data = json.loads(line)
    if checkMandatoryFieldsInJSON(json_data):
        ip_address = json_data['Source'][0]['IP4'][0]
        for node in json_data['Node']:
            if not re.search("warden_filer", node['Name']):
                node_name = node['Name']
                break
        alert = node_name + "." + json_data['Category'][0]  + "_" + str(json_data['Target'][0]['Port'][0])
        time_of_alert = int(timegm(time.strptime(re.sub("( |T|\..*|\+.*|Z.*)", "", json_data['DetectTime']), "%Y-%m-%d%H:%M:%S")))
        return {"IP": ip_address, "alert": alert, "Time": time_of_alert}
    else:
        return None


def createSequenceDB():
    file = open(sys.argv[1], "r")
    db = {}
    for line in file:
        alert = parseLineOfJSON(line)
        if alert == None:
            continue
        if alert['IP'] not in db: # AK NIE JE ESTE V DB SEKVIENCIA (IP ADDRESSA)
            db[alert['IP']] = FastRBTree()
        isThereNode = db[alert['IP']].get(alert['Time'], None) #AK UZ V TOM CASE JE NIAKA UDALOST V SEKVENCII
        if isThereNode != None:
           if alert['alert'] not in isThereNode:
               isThereNode.append(alert['alert'])
        else:
           db[alert['IP']].insert(alert['Time'], [alert['alert']])

    return db


def checkTransition(nameOfTransition, transitions):
    if nameOfTransition in transitions:
        value = transitions[nameOfTransition]
        transitions[nameOfTransition] += 1
        return nameOfTransition + "_Transition" + str(value)
    else:
        transitions[nameOfTransition] = 0
        return nameOfTransition + "_Transition"


def addArcs(petriNet, nameOfAlert, ancestors, transitions): #ANCESTORS JE POLE PLACES(ICH NAZOV)
    if nameOfAlert not in petriNet:
        petriNet.add_place(Place(nameOfAlert))
    expression = 'x+"' + nameOfAlert + '"+","'
    for anc in ancestors:
        if anc == nameOfAlert:
           continue
        newTransition = checkTransition(nameOfAlert, transitions)
        petriNet.add_transition(Transition(newTransition))
        petriNet.add_input(anc, newTransition, Variable('x'))
        petriNet.add_output(nameOfAlert, newTransition, Expression(expression)) 


def createPetriNet(db):
    petriNet = PetriNet('net')
    petriNet.add_place(Place('Attacker'))
    transitions = {}
    for ip, sequence in db.items():
        ancestors = ['Attacker']
        for alerts in sequence.nsmallest(sequence.__len__):
            ancs = []
            for alert in alerts[1]:
                addArcs(petriNet, alert,  ancestors, transitions) 
                ancs.append(alert)
            ancestors = list(ancs)
    return petriNet


def logPath(parent, node, logs, attacker):
    rule = parent + " ==> " + node
    if rule in logs:
        logs[rule].add(attacker)
    else:
        logs[rule] = set()
        logs[rule].add(attacker)
    
    if parent not in logs["conf"]:
        logs["conf"][parent] = set()
        logs["conf"][parent].add(attacker)
    else:
        logs["conf"][parent].add(attacker)
    

def simulateAttackers(petriNet, numberOfAttempts, longOfSequence):
    print("SIMULATION STARTED")
    logs = {"conf": {}}
    for attacker in range(numberOfAttempts):
        petriNet.set_marking(Marking(Attacker=[""]))
        node = ["Attacker"]
        parent = "Attacker"
        for k in range(longOfSequence):
            isThereSuccessor = petriNet.post(node)
            if len(isThereSuccessor) == 0:
                break
            transition = random.choice(tuple(isThereSuccessor)) # UZOL MOZE MAT VIAC PRECHODOV
            tmpArray = [transition]    
            petriNet.transition(transition).fire(petriNet.transition(transition).modes()[0]) # PRECHOD MOZE MAT LEN JEDEN UZOL
            node = [petriNet.post(tmpArray).pop()]
            if parent == "Attacker": 
                parent = node[0]
                continue
            logPath(parent, node[0], logs, attacker)
            parent = node[0]
    return logs


def analyzeLogs(logs, numberOfAttempts, support, confidence):
    print("START ANALYZING LOGS")
    file = open(sys.argv[2], "w")
    for log in logs:
        if log == "conf":
           continue
        predicat = log.split(" ==> ")[0]
        if (len(logs[log])/numberOfAttempts >= support) and (len(logs[log])/len(logs["conf"][predicat]) >= confidence):
            file.write(log + " #SUPP: " + str(len(logs[log])/numberOfAttempts) + " (" + str(len(logs[log])) + "/" + str(numberOfAttempts) + ") #CONF: " + str(len(logs[log])/len(logs["conf"][predicat])) + "\n")


def init():
    db = createSequenceDB()
    net = createPetriNet(db)
    numberOfAttempts = int(sys.argv[3])
    longOfSequence = int(sys.argv[4])
    tresholdSupport = float(sys.argv[5])
    tresholdConfidence = float(sys.argv[6])
    logs = simulateAttackers(net, numberOfAttempts, longOfSequence) 
    print("FINISH SIMULATION")
    analyzeLogs(logs, numberOfAttempts, tresholdSupport, tresholdConfidence)
    print("DONE! YOUR PREDICTIONS ARE AVAILABLE IN FILE: " + sys.argv[2])

init()
