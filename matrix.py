import sys
import json

def createMatrix():
        matrix = []
        result = parseFile(matrix)
        #printMatrix(result) UNCOMMENT THIS LINE IF YOU WANT 2D FORMAT OF MATRIX
        json_data = json.dumps({"matrix": result[0], "preconditions": result[1], "privileges": result[2]}, indent=4)
        print(json_data)
        return json_data


def addNewPrerequisity(prerequisity, prerequisites, widthOfMatrix, matrix):
	prerequisites.append(prerequisity) # STRINGOVY ZOZNAM
	matrix.append([0 for _ in range(widthOfMatrix)])


def addNewPrivilege(privilege, privileges, matrix, indexes):
	for index, row in enumerate(matrix):
		if index in indexes:
			row.append(1)
		else:
		    row.append(0)
	privileges.append(privilege) # STRINGOVY ZOZNAM


def parseFile(matrix):
	file = open(sys.argv[1], "r")
        widthOfMatrix = 0
        heightOfMatrix = 0
        privileges = []
        prerequisites = []

	for line in file:
		tmpL, tmpR = line.split('==>')
		tmpL = tmpL.strip()
		startVertices = tmpL.split(',')

		indexes = [] # na ktory riadok dat 1
		for vertex in startVertices:
			isTherePrerequisity = prerequisites.index(vertex) if vertex in prerequisites else None
			if isTherePrerequisity != None:
                                indexes.append(isTherePrerequisity)
			else:
                                indexes.append(heightOfMatrix)
				heightOfMatrix += 1
				addNewPrerequisity(vertex, prerequisites, widthOfMatrix, matrix)

		endVertices, supp, conf = tmpR.split("#")
		endVertices = endVertices.strip()
		endVertices = endVertices.split(',')

		for vertex in endVertices:
			isTherePrivilege = privileges.index(vertex) if vertex in privileges else None
			widthOfMatrix += 1
			addNewPrivilege(vertex, privileges, matrix, indexes)
	return (matrix, prerequisites, privileges)




def printMatrix(matrix):
        print("MATRIX:")
        print("--- rows: " + str(len(matrix[1])))
        print("--- columns: " + str(len(matrix[2])))
        for row in matrix[0]:
                print(row)

createMatrix()
