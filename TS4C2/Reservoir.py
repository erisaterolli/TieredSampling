__author__ = 'erisa'
from helping_functions import *
import itertools
import random as rnd
#import numpy as np

class WedgeReservoir():
    def __init__(self, size, graph, edge_reservoir):
        self.M  = size
        self.unweighted_reservoir = {}
        self.triangles = []
        self.total_triangles = 0
        self.cliques = 0
        self.cliques_seen = 0
        self.graph = graph
        self.W = 0
        self.wedge_dic = {}
        self.triangle_estimator = 0
        self.edge_reservoir = edge_reservoir
        self.fourest_estimator = 0
        self.ordering = [0]*9

    def add_unweighted_reservoir(self,triangle, times):
        # self.triangles.append((triangle,times))
        a = triangle[0]
        b = triangle[1]
        c = triangle[2]
        tab = times[0]
        tac = times[1]
        tbc = times[2]
        if a in self.unweighted_reservoir:
            self.unweighted_reservoir[a].append((b,tab,c,tac,tbc))
        else:
            self.unweighted_reservoir[a]=[(b,tab,c,tac,tbc)]
        if b in self.unweighted_reservoir:
            self.unweighted_reservoir[b].append((a,tab,c,tbc,tac))
        else:
            self.unweighted_reservoir[b]=[(a,tab,c,tbc,tac)]
        if c in self.unweighted_reservoir:
            self.unweighted_reservoir[c].append((a,tac,b,tbc,tab))
        else:
            self.unweighted_reservoir[c]=[(a,tac,b,tbc,tab)]


    def delete_unweighted_reservoir(self, triangle, times, random_triangle):
        triangle_to_be_deleted = self.triangles[random_triangle][0]
        times_to_be_deleted = self.triangles[random_triangle][1]
        self.triangles[random_triangle]= (triangle,times)
        a = triangle_to_be_deleted[0]
        b = triangle_to_be_deleted[1]
        c = triangle_to_be_deleted[2]
        tab = times_to_be_deleted[0]
        tac = times_to_be_deleted[1]
        tbc = times_to_be_deleted[2]
        if len(self.unweighted_reservoir[a]) == 1:
            del self.unweighted_reservoir[a]
        else:
            self.unweighted_reservoir[a].remove((b,tab,c,tac,tbc))
        if len(self.unweighted_reservoir[b]) == 1:
            del self.unweighted_reservoir[b]
        else:
            self.unweighted_reservoir[b].remove((a,tab,c,tbc,tac))
        if len(self.unweighted_reservoir[c]) == 1:
            del self.unweighted_reservoir[c]
        else:
            self.unweighted_reservoir[c].remove((a,tac,b,tbc,tab))

    def sample_triangle(self, triangle, times):
        if self.total_triangles <= self.M:
            self.triangles.append((triangle,times))
            self.add_unweighted_reservoir(triangle, times)
        else:
            if rnd.random() < 1.0*self.M / self.total_triangles:
                random_triangle = rnd.randint(0,self.M-1)
                # random_tr = self.triangles[random_triangle][0]
                # random_times = self.triangles[random_triangle][1]
                self.delete_unweighted_reservoir(triangle, times,random_triangle)
                self.add_unweighted_reservoir(triangle, times)

    def update_cliques(self, u, v, edge_reservoir):

        is_u = u in self.unweighted_reservoir
        is_v = v in self.unweighted_reservoir
        if is_u and is_v:
            triangles_u = self.unweighted_reservoir[u]

            triangles_v = self.unweighted_reservoir[v]

            for tr_u in triangles_u:
                for tr_v in triangles_v:

                    if tr_u[0] == tr_v[0] and tr_u[2]== tr_v[2]:
                        # print u, triangles_u
                        # print v, triangles_v
                        t1 = tr_u[4]
                        t2 = tr_u[1]
                        t4 = tr_u[3]
                        t3 = tr_v[3]
                        t5 = tr_v[1]

                        self.cliques_seen += 1
                        p = self.cliques_probability(t1, t2, t3, t4, t5)

                        self.cliques += 1.0/p


    def cliques_probability(self,  t1,  t2,  t3,  t4, t5):
        max1 = max(t2, t4)
        min1 = min(t2, t4)
        max2 = max(t3, t5)
        min2 = min(t3, t5)
        p1 = 0
        p11 = min(1.0, 1.0*(self.M - 1)/(self.total_triangles - 1))
        p2 = min(1.0, (1.0*self.M/self.total_triangles)) * min(1.0, 1.0*self.edge_reservoir.M/(max(t1, max2)-1)) * min(1.0, 1.0*(self.edge_reservoir.M - 1)/(max(t1,max2) - 2))
        if t1 > max(t2, t3, t4, t5):
            self.ordering[0]+=1
            p1 = min(1.0, (self.edge_reservoir.M - 3.0)/(t1 - 4)) * min(1.0, 1.0*(self.edge_reservoir.M - 2)/(t1 - 3))
        elif max2 > t1 > max(max1, min1, min2):
            self.ordering[1]+=1
            p1 = min(1.0, (self.edge_reservoir.M - 2.0)/(t1 - 3)) * min(1.0, 1.0*(self.edge_reservoir.M - 1)/(t1 - 2))
        elif max2 > max1 > max(min1, min2, t1):
            self.ordering[2]+=1
            p1 = min(1.0, (self.edge_reservoir.M - 2.0)/(max1 - 3))
        elif max2 > min2 > t1 > max(max1, min1):
            self.ordering[3]+=1
            p1 = min(1.0, (self.edge_reservoir.M - 1.0)/(t1 - 2)) * min(1.0, 1.0*(self.edge_reservoir.M)/(t1 - 1))
        elif max2 > min2 > max1 > max(t1, min1):
            self.ordering[4]+=1
            p1  = min(1.0, (self.edge_reservoir.M - 1.0)/(max1 - 2))
        elif max1 > t1 > max(min1, max2, min2):
            self.ordering[5]+=1
            p1 = min(1.0, (self.edge_reservoir.M - 1.0)/(max1 - 2)) * min(1.0, (self.edge_reservoir.M - 2.0)/(t1 - 3)) * min(1.0, 1.0*max(self.edge_reservoir.M, t1 - 1)/(max1 - 1))
        elif max1 > max2 > max(t1, min1, min2):
            self.ordering[6]+=1
            p1 = min(1.0, 1.0*max(self.edge_reservoir.M, max2 - 2)/(max1 - 2)) *min(1.0, 1.0*max(self.edge_reservoir.M, max2 - 1)/(max1 - 1)) * min(1.0, (self.edge_reservoir.M - 2.0)/(max2 - 3))
        elif max1 > min1 > t1 > max2 > min2:
            self.ordering[7]+=1
            p1 = min(1.0, (self.edge_reservoir.M - 1.0)/(max1 - 2)) * min(1.0, 1.0*(self.edge_reservoir.M)/(max1 - 1))
        else:
            self.ordering[8]+=1
            p1 = min(1.0, (self.edge_reservoir.M - 1.0)/(max1 - 2)) * min(1.0, 1.0*max(self.edge_reservoir.M,max2 - 1)/(max1 - 2))

        return p11*p1 * p2

    def update_triangles(self, u, v):
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
                times = [self.edge_reservoir.total_edges,self.graph.graph_structure[a][c], self.graph.graph_structure[b][c]]
            elif a == mini and c == maxi:
                times = [self.graph.graph_structure[a][b],self.edge_reservoir.total_edges, self.graph.graph_structure[b][c]]
            else:
                times = [self.graph.graph_structure[a][b],self.graph.graph_structure[a][c],self.edge_reservoir.total_edges]
            self.sample_triangle(tuple(triangle), times )
    def get_number_squares(self):
        return self.cliques




