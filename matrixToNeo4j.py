from py2neo import Graph, Node, Relationship
import sys
import json

relationships = []

def visualize():
    global relationships
    with open(sys.argv[1]) as json_file:  
        json_data            = json.load(json_file)
        createdAllPrivileges = False
        tmpPreconditions     = {}
        tmpPrivileges        = {}
        attacker             = Node("Attacker", name="Attacker")
        
        for index, nameP in enumerate(json_data["preconditions"]): # CREATE ALL PRECONDITIONS
            tmpPreconditions[index] = (Node("Precondition", name=nameP))
            relationships.append(Relationship(attacker, "_", tmpPreconditions[index]))

        for i, precondition in enumerate(json_data["preconditions"]):
            for k, privilege in enumerate(json_data["privileges"]):
                if createdAllPrivileges == False: tmpPrivileges[k] = Node("Conclusion", name=privilege)  # CREATE ALL CONCLUSIONS
                if json_data["matrix"][i][k] == 1:
                    relationships.append(Relationship(tmpPreconditions[i], "_", tmpPrivileges[k])) # IF THERE IS RELATIONSHIP ADD IT
                if precondition == privilege:
                        relationships.append(Relationship(tmpPrivileges[k], "backward", tmpPreconditions[i])) # IF THERE IS BACKWARD EDGE ADD IT
            createdAllPrivileges = True
        




def createGraph():
    global relationships

    graph = Graph()
    graph.delete_all()
    visualize()
    for relationship in relationships:
        graph.create(relationship) 


createGraph()
