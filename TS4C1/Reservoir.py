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
        self.seen = []

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
            # seen = False
            for tr_u in triangles_u:
                a = tr_u[0]
                b = tr_u[2]
                t1= tr_u[4]
                t2 = tr_u[1]
                t3 = tr_u[3]
                cl = sorted([u,v,a,b])
                if a in self.graph.graph_structure and b in self.graph.graph_structure:
                    if v in self.graph.graph_structure[a] and v in self.graph.graph_structure[b]: #clique formation
                        t4 = self.graph.graph_structure[a][v]
                        t5 = self.graph.graph_structure[b][v]
                        p = self.cliques_probability(t1, t2, t3, t4, t5,self.edge_reservoir.total_edges)
                        self.cliques += 0.5/p
                        if cl not in self.seen:
                            self.seen.append(cl)
                        # self.cliques_seen += 1
            for tr_v in triangles_v:
                a = tr_v[0]
                b = tr_v[2]
                t1= tr_v[4]
                t2 = tr_v[1]
                t3 = tr_v[3]
                cl = sorted([u,v,a,b])
                if a in self.graph.graph_structure and b in self.graph.graph_structure:
                    if u in self.graph.graph_structure[a] and u in self.graph.graph_structure[b]: #clique formation
                        t4 = self.graph.graph_structure[a][u]
                        t5 = self.graph.graph_structure[b][u]
                        p = self.cliques_probability(t1, t2, t3, t4, t5, self.edge_reservoir.total_edges)
                        self.cliques += 0.5/p
                        if cl not in self.seen:
                            self.seen.append(cl)


    def cliques_probability(self, t1, t2, t3, t4, t5, t6):
        last_tr = max(t1, t2, t3, self.edge_reservoir.M + 1)
        last_ed = max(t4, t5)
        p2 = min(1, 1.0*self.M/ self.total_triangles) * (1.0*self.edge_reservoir.M/(last_tr-1)) * (1.0 * (self.edge_reservoir.M-1)/(last_tr - 2))
        p1 = 0
        if t6 <= self.edge_reservoir.M:
            p1 = 1
        elif min(t4, t5) > last_tr:
            p1 = 1.0*self.edge_reservoir.M / (t6 - 1) * (1.0*self.edge_reservoir.M - 1) / (t6 - 2)
        elif last_ed > last_tr > min(t4, t5):
            p1 = (1.0 * (self.edge_reservoir.M - 1)/(t6 - 2))*(1.0*(self.edge_reservoir.M - 2)/(last_tr - 3))*(1.0*(last_tr - 1)/ (t6 - 1))
        else:
            p1 = (1.0*(self.edge_reservoir.M - 2)/(last_tr - 3)) * (1.0*(self.edge_reservoir.M - 3)/(last_tr - 4)) * (1.0*(last_tr - 1)/ (t6 - 1))*(1.0*(last_tr - 2)/ (t6 - 2))
        print self.edge_reservoir.total_edges, self.M, self.total_triangles, self.edge_reservoir.M, t1, t2, t3, t4, t5, t6, p1, p2
        return p1*p2

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




