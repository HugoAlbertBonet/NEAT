import numpy as np
import random
import itertools
from sklearn.cluster import AgglomerativeClustering, SpectralClustering
from enum import Enum

class Connection:
    def __init__(self, connection_id, node_in, node_out, weight, enabled = True):
        self.node_in = node_in
        self.node_out = node_out
        self.weight = weight
        self.enabled = enabled
        self.id = connection_id

    def disable(self): 
        self.enabled = False


class NodeType(Enum):
        INPUT = 1
        OUTPUT = 2
        HIDDEN = 3

class Node:
    def __init__(self, node_id, node_type):
        self.id = node_id
        self.type = node_type

    def copy(self):
        return Node(self.id, self.type)

class Network:
    def __init__(self, inputs, outputs):
        self.nodes = []
        self.connections = {}
        self.inputs = inputs
        self.outputs = outputs
        self.hidden = 0
        for i in range(inputs):
            self.nodes.append(Node(i, NodeType.INPUT))
        for i in range(outputs):
            self.nodes.append(Node(len(self.nodes), NodeType.OUTPUT))
            for j in range(inputs):
                self.connections[(j, len(self.nodes)-1)] = Connection(len(self.connections), self.nodes[j], self.nodes[-1], random.uniform(-1,1))

        
    

class NEAT:

    def __init__(self,time_deadline,problem_path,init="cluster",mode="agglomerative",**kwargs): 
        """
        Initialize an instance of class GA given a time deadline and an instance path.

        :param time_deadline: Max time of the execution.
        :type time_deadline: int
        :param problem_path: Path to a certain instance.
        :type problem_path: str
        :param init: Parameter to use cluster initialization or not.
        :type init: str
        :param mode: Specific parameter that indicates the mode of the clusters.
        :type mode: str
        """
        self.problem_path = problem_path
        self.best_solution = None 
        self.time_deadline = time_deadline 
        self.best_fitness = None
        self.init = init
        self.mode = mode
        self.n_vehicles = None

        self.evolution = []

    def crossover(self, parent1, parent2):
        child = Network(parent1.inputs, parent1.outputs)
        if len(parent1.nodes) > len(parent2.nodes):
            child.nodes = [node.copy() for node in parent1.nodes]
        else: 
            child.nodes = [node.copy() for node in parent2.nodes]
        for index, con in parent1.connections.items():
            if index in parent2.connections:
                if parent2.connections[index].enabled and con.enabled:
                    child.connections[index] = Connection(len(child.connections), child.nodes[parent1.connections[index].node_in.id], child.nodes[parent1.nodes[-1].id], weight= parent1.connections[index].weight) if random.random() > 0.5 else Connection(len(child.connections), child.nodes[parent2.connections[index].node_in.id], child.nodes[parent2.nodes[-1].id], weight= parent2.connections[index].weight)
                else: child.connections[index] = Connection(len(child.connections), child.nodes[parent1.connections[index].node_in.id], child.nodes[parent1.nodes[-1].id], weight=random.uniform(-1,1), enabled=False)

            else: child.connections[index] = Connection(len(child.connections), child.nodes[parent1.connections[index].node_in.id], child.nodes[parent1.nodes[-1].id], weight= parent1.connections[index].weight)

        for index, con in parent2.connections.items():
            if index not in parent1.connections: 
                child.connections[index] = Connection(len(child.connections), child.nodes[parent2.connections[index].node_in.id], child.nodes[parent2.nodes[-1].id], weight= parent2.connections[index].weight)

        return child

    def mutation_node(self, parent):
        while True:
            i = random.randint(0, len(parent.connections) - 1)
            j = random.randint(i+1, len(parent.connections) - 1)
            if parent.connections[(i, j)].enabled:
                break
        parent.nodes.append(Node(len(parent.nodes), NodeType.HIDDEN))
        parent.hidden += 1
        parent.connections[(i, j)].disable()
        parent.connections[(parent.connections[(i, j)].node_in.id, parent.nodes[-1].id)] = Connection(len(parent.connections), parent.connections[(i, j)].node_in, parent.nodes[-1], weight=random.uniform(-1,1))
        parent.connections[(parent.nodes[-1].id, parent.connections[(i, j)].node_out.id)] = Connection(len(parent.connections), parent.nodes[-1], parent.connections[(i, j)].node_out, weight=random.uniform(-1,1))


    def mutation_connection(self, parent):
        while True:
            a, b = random.randint(0, len(parent.nodes)-1), random.randint(0, len(parent.nodes) - 1)
            if a != b and (a, b) not in parent.connections:
                break
        parent.connections[(a, b)] = Connection(len(parent.connections), parent.nodes[a], parent.nodes[b], weight=random.uniform(-1,1))
        

    def mutation_weight(self, parent):
        i = random.randint(0, len(parent.connections) - 1)
        j = random.randint(i + 1, len(parent.connections) - 1)
        parent.connections[(i, j)].weight = random.uniform(-1,1)

