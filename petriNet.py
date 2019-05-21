from snakes.nets import *
import json
import sys

graph = PetriNet('First net')
graph.add_transition(Transition("Attacker"))
err = {}
preconditions = {}

def parseFile(data):
	global graph, err, preconditions
	file = data.split("\n")[:-1]
	for line in file:
		tmpL, tmpR = line.split('==>')
		tmpL = tmpL.strip()
		startVertices = tmpL.split(',')
		for vertex in startVertices:
			if vertex not in preconditions:
				nameOfVertex = ""
				if vertex not in err:
					nameOfVertex = vertex
					err[vertex] = 1
				else:
					nameOfVertex = vertex + "_(" + str(err[vertex]) + ")"
					err[vertex] += 1
				preconditions[vertex] = nameOfVertex
				graph.add_place(Place(nameOfVertex))
				graph.add_output(nameOfVertex, "Attacker", Expression('x'))
		endVertices, supp, conf = tmpR.split("#")
		endVertices = endVertices.strip()
		endVertices = endVertices.split(',')
		for vertex in endVertices:
			nameOfTransition = ""
			if vertex not in err:
				nameOfTransition = vertex
				err[vertex] = 1
			else:
				nameOfTransition = vertex + "_(" + str(err[vertex]) + ")"
				err[vertex] += 1
			
			graph.add_transition(Transition(nameOfTransition))
			for ver in startVertices:
				graph.add_input(preconditions[ver], nameOfTransition, Variable('x'))
			nameOfNode = vertex + "_(" + str(err[vertex]) + ")"
			err[vertex] += 1
			graph.add_place(Place(nameOfNode))
			graph.add_output(nameOfNode, nameOfTransition, Expression(vertex))





def init():
	data = open(sys.argv[1], "r") 
	a = data.read()
	parseFile(a)
	return graph

init()
