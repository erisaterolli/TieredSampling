__author__ = 'erisa'
import random as rnd
import itertools
import math
#import numpy as np
#from helping_functions import *
class EdgeReservoir():
    def __init__(self, size, graph, res_size):
        self.M = size
        self.reservoir = []
        self.total_edges = 0
        self.graph = graph
        self.cliques = 0
        self.total_triangles = 0
        self.triangles_seen = []
        self.cliques_seen = 0
        self.memory = res_size
        self.limit = self.memory/3.0

    def setM(self, newM):
        self.M = newM

    def getM(self):
        return self.M

    def getCliquesEstimator(self):
        return self.cliques

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

    def update_cliques(self, u, v, t):
        if u in self.graph.graph_structure and v in self.graph.graph_structure:
            common_neighbors = self.graph.get_common_neighbors(u,v)
            c = 0
            for a,b in itertools.combinations(common_neighbors,2):
                    if a != b and b in self.graph.graph_structure[a]:
                        c += 1
                        self.cliques_seen += 1
            p = min(1.0, 1.0*self.M/(t-1))\
                *min(1.0, (1.0*self.M-1)/(t-2))\
                *min(1.0, 1.0*(self.M-2)/(t-3))\
                *min(1.0, 1.0*(self.M-3)/(t-4))\
                *min(1.0, 1.0*(self.M-4)/(t-5))
            p_clique = max(1.0, 1.0/p)
            self.cliques+= p_clique*c

    def update_triangles(self, u, v, t, res_size):
        common_neighbors = self.graph.get_common_neighbors(u,v)
        for x in common_neighbors:
            self.total_triangles += 1
            triangle = sorted([u,v,x])
            a = triangle[0]
            b = triangle[1]
            c = triangle[2]
            mini = min(u,v)
            maxi = max(u,v)
            if a == mini and b == maxi:
                times = [t,self.graph.graph_structure[a][c], self.graph.graph_structure[b][c]]
            elif a == mini and c == maxi:
                times = [self.graph.graph_structure[a][b],t, self.graph.graph_structure[b][c]]
            else:
                times = [self.graph.graph_structure[a][b],self.graph.graph_structure[a][c],t]
            if self.total_triangles < self.limit:
                self.triangles_seen.append(((a,b,c), times))

    def shrinkByAlpha(self, alpha):
        to_be_delete = int(math.floor(self.M * alpha))
        l  = len(self.reservoir)
        for i in xrange(to_be_delete):
            x = rnd.randint(0, l - 1)
#            print x
            to_be_deleted = self.reservoir[x]
            if x == l-1:
                self.reservoir.pop()
            else:
                self.reservoir[x] = self.reservoir[l - 1]
                self.reservoir.pop()
            # del self.reservoir[x]
            self.graph.remove_edge(to_be_deleted[0], to_be_deleted[1])
            l -= 1
            self.M -= 1
        return to_be_delete
    def shrinkByNumber(self, number):
        l  = len(self.reservoir)
        for i in xrange(number):
            x = rnd.randint(0, l - 1)
            to_be_deleted = self.reservoir[x]
            if x == l-1:
                self.reservoir.pop()
            else:
                self.reservoir[x] = self.reservoir[l - 1]
                self.reservoir.pop()
            # del self.reservoir[x]
            self.graph.remove_edge(to_be_deleted[0], to_be_deleted[1])
            l -= 1
            self.M -= 1



