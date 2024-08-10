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
        pass

    def mutation_node(self, parent):
        while True:
            i = random.randint(0, len(parent.connections) - 1)
            if parent.connections[i].enabled:
                break
        parent.nodes.append(Node(len(parent.nodes), NodeType.HIDDEN))
        parent.connections[i].disable()
        parent.connections.append(Connection(len(parent.connections), parent.connections[i].node_in, parent.nodes[-1], weight=random.uniform(-1,1)))
        parent.connections.append(Connection(len(parent.connections), parent.nodes[-1], parent.connections[i].node_out, weight=random.uniform(-1,1)))


    def mutation_connection(self, parent):
        pass

    def mutation_weight(self, parent):
        pass