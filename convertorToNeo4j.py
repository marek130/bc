from py2neo import Graph, Node, Relationship
import sys

graph = Graph()

nodes    	  = {}
companies	  = {}
relationships = []

def parseFile():
	global nodes, companies, relationships
	file = open(sys.argv[1], "r")
	
	for line in file:
		tmpL, tmpR = line.split('==>')
		tmpL = tmpL.strip()
		startVertices = tmpL.split(',')
		mergeNode = Node("Merge", name = "Merge node")

		for vertex in startVertices:
			companyOfNode = ".".join(vertex.split(".")[:-2])
			nameOfNode 	  = vertex.split(".")[-2:-1][0]
			attempt       = vertex.split(".")[-1]
			a = "Company_" + companyOfNode.replace(".", "_")
			if companyOfNode not in companies:
				nodes[companyOfNode] 	 = {}
				companies[companyOfNode] = Node("COMPANY", a, name = companyOfNode)
			if nameOfNode not in nodes[companyOfNode]:
				nodes[companyOfNode][nameOfNode] = Node("Node", a, name = nameOfNode, company = companyOfNode)
				relationships.append(Relationship(companies[companyOfNode], a, nodes[companyOfNode][nameOfNode]))
			relationships.append(Relationship(nodes[companyOfNode][nameOfNode], attempt, mergeNode, whatAttempt = attempt))

		endVertices, supp, conf = tmpR.split("#")
		endVertices = endVertices.strip()
		endVertices = endVertices.split(',')
		for vertex in endVertices:
			companyOfNode = ".".join(vertex.split(".")[:-2])
			nameOfNode    = vertex.split(".")[-2:-1][0]
			attempt       = vertex.split(".")[-1]
			a = "Company_" + companyOfNode.replace(".", "_")
			if companyOfNode not in companies:
				nodes[companyOfNode] 	 = {}
				companies[companyOfNode] = Node("Company", a, name = companyOfNode) 
			if nameOfNode not in nodes[companyOfNode]:
				nodes[companyOfNode][nameOfNode] = Node("Node", a, name = nameOfNode, company = companyOfNode)
				relationships.append(Relationship(companies[companyOfNode], a , nodes[companyOfNode][nameOfNode]))
			relationships.append(Relationship(mergeNode, attempt , nodes[companyOfNode][nameOfNode], conf = conf, whatAttempt = attempt))

def createGraph():	
	for relationship in relationships:
		graph.create(relationship)


graph.delete_all()
parseFile()
createGraph()
