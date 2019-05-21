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
		nameForNode = node["Category"] + "_" + node["NodeName"] + "_" + node["Port"]
		objectNode =  Node("node", name=nameForNode)
		nodesList[nameForNode] = objectNode
		relationships.append(Relationship(ATTACKER, "_", objectNode))

	for node in data["StartNodes"]: # dict [NAME => OBJECT]
		nameNode = node["Category"] + "_" + node["NodeName"] + "_" + node["Port"]
		for predication in node["Predictions"]:
			nameForPredicate = predication["Category"] + "_" + predication["NodeName"] + "_" + predication["Port"]
			predicatis = Node("Predication", name=nameForPredicate, predict=True, conf=predication["CONF"])
			relationships.append(Relationship(nodesList[nameNode], "_", predicatis))
			for dependsNode in predication["DependsAlsoOn"]:
				matchName = dependsNode["Category"] + "_" + dependsNode["NodeName"] + "_" + dependsNode["Port"]
				for key, currentNode in nodesList.items():
						if key == matchName:
							relationships.append(Relationship(currentNode, "_", predicatis))
			for nodis in data["StartNodes"]:
				reverseNodeName = nodis["Category"] + "_" + nodis["NodeName"] + "_" + nodis["Port"]
				if reverseNodeName == nameForPredicate:
					relationships.append(Relationship(predicatis, "I", nodesList[reverseNodeName]))



def createGraph():	
	for relationship in relationships:
		graph.create(relationship)


graph.delete_all()
parseFile()
createGraph()
