from __future__ import division
from functools import reduce
import sys
import json
import re
import time
from bintrees import FastRBTree
from calendar import timegm


class Graph:
    def __init__(self, root):
        self.root = root
        self.hasMap = {}  # { "NAZOV_UZLA" : OBJEKT}

    def getRoot(self):
        return self.root

    def containNode(self, root, node):
        
        if node in root.children:
            return (True, root) # vrati Rodica
        for child in root.children:
            contain = self.containNode(child, node)
            if contain[0] == True:
                return (True, contain[1])
        return (False, None)
         
    def addToHashMap(self, node):
        self.hasMap[node.name] = node
   
    def getFromHashMap(self, nameOfNode):
        if nameOfNode in self.hasMap:
           return self.hasMap[nameOfNode]
        return None

class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.visited = False
        self.ancestors = FastRBTree()
    

    def updateChildren(self, child, nameOfSequence):
        if child in self.children:
            self.children[child].add(nameOfSequence)
        else:
            self.children[child] = set()
            self.children[child].add(nameOfSequence)

    def getChild(self, nameOfChild):
        return filter(lambda x: x == nameOfChild, self.children.keys())

    def updateAncestors(self, ancestors, nameOfSequence):
        for ancestor in ancestors:
            if self.name == ancestor.name:
                continue
            elementFromTree = self.ancestors.get(ancestor.name, None)
            if elementFromTree != None:
                elementFromTree.add(nameOfSequence)
                self.ancestors.__setitem__(ancestor.name, elementFromTree)
            else: # NIE JE V SEK
                tmpValue = set()
                tmpValue.add(nameOfSequence)
                self.ancestors.insert(ancestor.name, tmpValue)
    


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



def createGraph(db):
    print("CREATING GRAPH")
    graph = Graph(Node("Attacker"))
    ancestors = [graph.getRoot()]
    graph.addToHashMap(graph.getRoot())
    conf = {}

    for ip, sequence in db.items():
        negative_cycle = False
        ancestors = [graph.getRoot()]
        path = []
        for alerts in sequence.nsmallest(sequence.__len__):
           ancs = [] # BUDUCI PREDKOVIA
           for alert in alerts[1]:
              if alert in conf:
                 conf[alert].add(ip) 
              else:
                 conf[alert] = set()
                 conf[alert].add(ip)
              node = graph.getFromHashMap(alert) 
              if node == None:
                 node = Node(alert)
                 graph.addToHashMap(node)
                 negative_cycle = False
              tmpAncs = filter((lambda ancestor: ancestor.name  == node.name), ancestors)
              if tmpAncs:   
                 ancs.append(tmpAncs[0])
                 continue
              if (node in path and negative_cycle == True):
                 map(lambda x: x.updateChildren(node, ip), ancestors)
               #  path.append(node)
                 node.updateAncestors(path, ip)
                 ancs.append(node)
                 continue
              if node in path:
                 map(lambda x: x.updateChildren(node, ip), ancestors)
                 negative_cycle = True
                 node.updateAncestors(path, ip)
              #   path.append(ancs)
                 ancs.append(node)
                 continue
              else:
                 negative_cycle = False
             # path.append(node)
              node.updateAncestors(path, ip)
              map(lambda x: x.updateChildren(node, ip), ancestors)
              ancs.append(node)
           ancestors = ancs
           path += list(ancs)
    return (graph, conf)


def foo(items, node, confHash, totalSeq, conf, number):
   print("XXX")
   names = [o[0] for o in items]
   tmpConf =  reduce((lambda x, y: x.intersection(y)), (o[1] for o in items))
   tmpNames = reduce((lambda x, y: x + "," + y), names)
   aa = list(names)
   aa.append(node.name)
   tmpDelimeterConf = map((lambda x: confHash[x]), aa)
   final = len(tmpConf.intersection(confHash[node.name]))

   if final/totalSeq >= number and final/len(set.intersection(*tmpDelimeterConf)) >= conf:
      return tmpNames + " ==> " + node.name + " #SUPP: " + str(final/totalSeq) + " (" + str(final) + "/" + str(totalSeq) + ") #CONF: " + str(final/len(set.intersection(*tmpDelimeterConf)))
   return ""


def makePermutation(array, node, confHash, totalSeq, conf, number, result):
    print("YYY")
    b = []
    for length in range(1, len(array)):
       if length > 2:
          break
       b += map(lambda x: foo(x, node, confHash, totalSeq, conf, number), list(itertools.combinations(array, length)))
    print(b)



def findNodeThanMore(node, totalSeq, confHash, conf, number, result):
    node.visited = True 
    for child in node.children:
       if child.visited == True:
          continue
       else:
          ancs = child.ancestors.nsmallest(child.ancestors.__len__)
          for a, v in ancs:
              if a != "Attacker" and (len(v)/len(confHash[a]) >= conf and len(v)/totalSeq >= number):
                 result.add(a + " ==> " + child.name + " (" + str(len(v)) + "/" + str(totalSeq) + ") #CONF: " + str(len(v)/len(confHash[a])))
          findNodeThanMore(child, totalSeq, confHash, conf, number, result)
    return result



def createRules(graph, totalSeq, confHash, support, confidence):
    result = findNodeThanMore(graph.getRoot(), totalSeq, confHash, confidence, support, set())
    print(len(result))
    return result



def writeRulesToFIle(rules):
   file = open(sys.argv[2], "w")
   for rule in rules:
       file.write(rule + "\n")


tmpDB = createSequenceDB()
print(len(tmpDB))
start = time.time()
graph,conf = createGraph(tmpDB)
print(len(graph.hasMap))
rules = createRules(graph, len(tmpDB), conf, 0.0006, 0.5)
end = time.time()
print(end - start)
writeRulesToFIle(rules)
