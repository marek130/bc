from snakes.nets import *
import json

graph = PetriNet('First net')
graph.add_transition(Transition("Attacker"))
err = 1

def parseFile(data):
	global graph, err
	file = data.split("\n")[:-1]
	for line in file:
		currentNodes = []
		currentPredictions = []
		tmpL, tmpR = line.split('==>')
		tmpL = tmpL.strip()
		startVertices = tmpL.split(',')
		for vertex in startVertices:
			print vertex
			if not graph.has_place(vertex):
				graph.add_place(Place(vertex))
				graph.add_output(vertex, "Attacker", Variable('p'))
		endVertices, supp, conf = tmpR.split("#")
		conf = float(conf.split(" ")[1].rstrip())
		conf = str(conf).replace(".","")
		endVertices = endVertices.strip()
		endVertices = endVertices.split(',')
		for vertex in endVertices:
			if not graph.has_transition(vertex.upper()):
				graph.add_transition(Transition(vertex.upper(),  Expression('p>0.5')))
				for ver in startVertices:
					print ver
					graph.add_input(ver, vertex.upper(), Variable("Conf" + conf))
			else:
				graph.add_transition(Transition(vertex.upper() + str(err),  Expression('p>0.5')))
				for ver in startVertices:
					graph.add_input(ver, vertex.upper() + str(err), Variable("Conf" + conf))
				err += 1
			if graph.has_place(vertex):
				graph.add_output(vertex, vertex.upper(), Variable('p'))




def init():
	data = open("data", "r") 
	a = data.read()
	parseFile(a)

init()
