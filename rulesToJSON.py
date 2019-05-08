import json
import sys
import copy

data = {"START_NODES": []}


def findIfThereIs(category, nodeName, port):
	global data

	for node in data["START_NODES"]:
		if node["NodeName"] == nodename and node["Category"] == category and node["Port"] == port:
			return True
	return False


def generateNodeContext(node):
	global data

	nodename, category, port = node.split("_")
	tmp = {"NodeName": nodename, "Category": category, "Port": port, "CONF": 1, "Predictions": [],
		   "DependsAlsoOn": []}
	return (findIfThereIs(category, nodename, port), tmp)


def parseFile():
	global data

	file = open(sys.argv[1], "r")

	for line in file:
		currentNodes = []
		currentPredictions = []
		tmpL, tmpR = line.split('==>')
		tmpL = tmpL.strip()
		startVertices = tmpL.split(',')

		for vertex in startVertices:
			(wasThere, node) = generateNodeContext(vertex)
			node.pop("DependsAlsoOn")
			t = (node, wasThere)
			currentNodes.append(t)

		endVertices, supp, conf = tmpR.split("#")
		conf = float(conf.split(" ")[1].rstrip())
		endVertices = endVertices.strip()
		endVertices = endVertices.split(',')

		for vertex in endVertices:
			(nezaujimaMaTo, attack) = generateNodeContext(vertex)
			attack["CONF"] = conf
			currentPredictions.append(attack)

		for node, wasThere in currentNodes:
			mainNodeCopy = copy.deepcopy(node)
			dependsNodes = []
			currentNodesCopy = copy.deepcopy(currentNodes)
			# DEPENDSALSOON
			for nodeCopy, _tmp in currentNodesCopy:  # list terajsich zaciatocnych uzlov bez aktualneho v loope
				if nodeCopy["NodeName"] != mainNodeCopy["NodeName"] or nodeCopy["Category"] != mainNodeCopy["Category"] or \
						nodeCopy["Port"] != mainNodeCopy["Port"]:
					_tmpNodeCopy = copy.deepcopy(nodeCopy)
					_tmpNodeCopy.pop("CONF")
					_tmpNodeCopy.pop("Predictions")
					dependsNodes.append(_tmpNodeCopy)
			listOfPredicitions = []  # zoznam predpovedi
			for prediction in currentPredictions:
				b = copy.deepcopy(prediction)
				b["DependsAlsoOn"] = dependsNodes  # kazdej predpovedi nastavim ze zavisi aj na druhych node okrem terajsieho v loope
				listOfPredicitions.append(b)
			if not wasThere:  # ak nebol uzol predtym v zaciatocnych tak ho prida
				mainNodeCopy["Predictions"] += listOfPredicitions
				data["START_NODES"].append(mainNodeCopy)
			else:
				for i in range(len(data["START_NODES"])):  # najde uzol ktory tam uz bol
					if data["START_NODES"][i]["NodeName"] == mainNodeCopy["NodeName"] and data["START_NODES"][i]["Category"] == \
							mainNodeCopy["Category"] and data["START_NODES"][i]["Port"] == mainNodeCopy["Port"]:
						data["START_NODES"][i]["Predictions"] += listOfPredicitions
						break


def transitive():
	tmp = copy.deepcopy(data)
	result = {"START_NODES": []}
	for node in tmp["START_NODES"]:
		copyOfNode = copy.deepcopy(node)
		j = 0
		for prediction in node["Predictions"]:
			copyOfPrediction = copy.deepcopy(prediction)
			for nextNode in tmp["START_NODES"]:
				copyOfNextNode = copy.deepcopy(nextNode)
				if copyOfPrediction["NodeName"] == copyOfNextNode["NodeName"] and copyOfPrediction["Category"] == copyOfNextNode[
					"Category"] and copyOfPrediction["Port"] == copyOfNextNode["Port"]:
					newPredictions = copy.deepcopy(copyOfNextNode["Predictions"])
					i = 0
					for pred in newPredictions:
						tmpValue = pred["CONF"] *copyOfPrediction["CONF"]
						if tmpValue < 0.5:
							newPredictions.pop(i)
						else:
							newPredictions[i]["CONF"] = tmpValue
						i += 1
					copyOfPrediction["Predictions"] += newPredictions
			copyOfNode["Predictions"][j]["Predictions"] = copyOfPrediction["Predictions"]
			j += 1
		tmpNewNode = copyOfNode
		result["START_NODES"].append(tmpNewNode)
	return result


parseFile()
finalVersion = transitive()
tmp = json.dumps(finalVersion)
parsed = json.loads(tmp)
print(json.dumps(parsed, indent=4, sort_keys=True))
