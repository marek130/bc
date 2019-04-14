from py2neo import Graph, Node, Relationship
import sys

graph = Graph()
globalPreconditions = {}
globalConclusions   = {}
relationships = []

def parseFile():
	global globalPreconditions, globalConclusions, relationships
	file = open(sys.argv[1], "r")
	
        attacker = Node("Attacker", name="attacker")
	for line in file:
                currentPreconditions = []
		preconditions, conclusions = line.split('==>')
		preconditions = preconditions.strip()
		startVertices = preconditions.split(',')
                
                for vertex in startVertices:
                        if vertex not in globalPreconditions:
                                globalPreconditions[vertex] = Node("Precondition", name=vertex)
                                relationships.append(Relationship(attacker, "_", globalPreconditions[vertex]))
			currentPreconditions.append(globalPreconditions[vertex])

		endVertices, supp, conf = conclusions.split("#")
		endVertices = endVertices.strip()
		endVertices = endVertices.split(',')
		for vertex in endVertices:
                        if vertex not in globalConclusions:
                                globalConclusions[vertex] = []
                        globalConclusions[vertex].append(Node("Conclusion", name=vertex, support=supp, confidence=conf))
                        for precondition in currentPreconditions:
				relationships.append(Relationship(precondition, "_" , globalConclusions[vertex][-1]))



def addBackwardEdges():
        global globalPreconditions, globalConclusions, relationships
        for conclusion in globalConclusions:
                if conclusion in globalPreconditions:
                        for vertex in globalConclusions[conclusion]:
                                relationships.append(Relationship(vertex, "backward", globalPreconditions[conclusion]))



def createGraph():	
	for relationship in relationships:
		graph.create(relationship)


graph.delete_all()
parseFile()
addBackwardEdges()
createGraph()
