__author__ = 'erisa'
import random as rnd
#import numpy as np
#from helping_functions import *
class EdgeReservoir():
    def __init__(self, size, graph):
        self.M = size
        self.reservoir = []
        self.total_edges = 0
        self.graph = graph

    def add_reservoir(self, u,v,t):#add in form(smallest,largest)
        if u>v:
            u,v = v, u
        self.reservoir.append((u,v,t))
        self.graph.add_edge(u, v, t)


    def delete_reservoir(self, u,v,t, to_be_deleted):
        edge_to_be_deleted = self.reservoir[to_be_deleted]
        if u>v:
            u,v = v, u
        self.reservoir[to_be_deleted] = (u,v,t)
        self.graph.remove_edge(edge_to_be_deleted[0], edge_to_be_deleted[1])

    def sample_edge(self, u,v,t):
        if self.total_edges <= self.M:
            self.add_reservoir(u,v,t)
        else:
            threshold = 1.0*self.M/self.total_edges
            if rnd.random() < threshold:
                to_be_removed = rnd.randint(0, len(self.reservoir) - 1)
                self.delete_reservoir(u,v,t, to_be_removed)
                self.graph.add_edge(u, v, t)