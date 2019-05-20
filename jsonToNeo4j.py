from py2neo import Graph, Node, Relationship
import sys
import json

graph = Graph()

nodesList 	  = {}
companies	  = {}
relationships = []
ATTACKER      = Node("ATTACKER", name="attacker")

def parseFile():
	global relationships, ATTACKER
	json_data=open("./jsonData").read()
	data = json.loads(json_data)

	for node in data["StartNodes"]:
		nameForNode = node["Company"] + "_" + node["Name"] + "_" + node["Event"]
		objectNode =  Node("node", name=nameForNode)
		nodesList[nameForNode] = objectNode
		relationships.append(Relationship(ATTACKER, "_", objectNode))

	for node in data["StartNodes"]: # dict [NAME => OBJECT]
		nameNode = node["Company"] + "_" + node["Name"] + "_" + node["Event"]
		for predication in node["Predictions"]:
			nameForPredicate = predication["Company"] + "_" + predication["Name"] + "_" + predication["Event"]
			predicatis = Node("Predication", name=nameForPredicate, predict=True, conf=predication["CONF"])
			relationships.append(Relationship(nodesList[nameNode], "_", predicatis))
			for dependsNode in predication["DependsAlsoOn"]:
				matchName = dependsNode["Company"] + "_" + dependsNode["Name"] + "_" + dependsNode["Event"]
				for key, currentNode in nodesList.items():
						if key == matchName:
							relationships.append(Relationship(currentNode, "_", predicatis))
			for nodis in data["StartNodes"]:
				reverseNodeName = nodis["Company"] + "_" + nodis["Name"] + "_" + nodis["Event"]
				if reverseNodeName == nameForPredicate:
					relationships.append(Relationship(predicatis, "I", nodesList[reverseNodeName]))



def createGraph():	
	for relationship in relationships:
		graph.create(relationship)


graph.delete_all()
parseFile()
createGraph()
