__author__ = 'erisa'
from helping_functions import *
import itertools
import random as rnd
#import numpy as np

class WedgeReservoir():
    def __init__(self, size, graph, edge_reservoir, estimator, total_memory):
        self.M  = size
        self.M_extra = 0
        self.unweighted_reservoir = {}
        self.triangles = [] #main triangle reservoir
        self.extra = [] # extra reservoir
        self.active_res = 1 # flag-> 1 triangle res, 2 extra res
        self.total_triangles = 0
        self.total_triangles_extra = 0
        self.cliques = estimator
        self.cliques_seen = edge_reservoir.cliques_seen
        self.graph = graph
        self.edge_reservoir = edge_reservoir
        self.memory = total_memory

    def add_unweighted_reservoir(self,triangle, times, res_size):
        # self.triangles.append((triangle,times,res_size))
        a = triangle[0]
        b = triangle[1]
        c = triangle[2]
        tab = times[0]
        tac = times[1]
        tbc = times[2]
        if a in self.unweighted_reservoir:
            self.unweighted_reservoir[a].append((b,tab,c,tac,tbc, res_size))
        else:
            self.unweighted_reservoir[a]=[(b,tab,c,tac,tbc,res_size)]
        if b in self.unweighted_reservoir:
            self.unweighted_reservoir[b].append((a,tab,c,tbc,tac,res_size))
        else:
            self.unweighted_reservoir[b]=[(a,tab,c,tbc,tac,res_size)]
        if c in self.unweighted_reservoir:
            self.unweighted_reservoir[c].append((a,tac,b,tbc,tab,res_size))
        else:
            self.unweighted_reservoir[c]=[(a,tac,b,tbc,tab,res_size)]


    def delete_unweighted_reservoir(self, a, b, c, tab, tac, tbc, time_deleted_triangle):

        if len(self.unweighted_reservoir[a]) == 1:
            del self.unweighted_reservoir[a]
        else:
            self.unweighted_reservoir[a].remove((b,tab,c,tac,tbc, time_deleted_triangle))
        if len(self.unweighted_reservoir[b]) == 1:
            del self.unweighted_reservoir[b]
        else:
            self.unweighted_reservoir[b].remove((a,tab,c,tbc,tac, time_deleted_triangle))
        if len(self.unweighted_reservoir[c]) == 1:
            del self.unweighted_reservoir[c]
        else:
            self.unweighted_reservoir[c].remove((a,tac,b,tbc,tab, time_deleted_triangle))

    def sample_triangle(self, triangle, times, res_size):
        if self.active_res == 1: #triangle reservoir is the active one, extra res is empty
            # print 'sample in triangles'
            if self.total_triangles <= self.M:
                self.triangles.append((triangle,times, res_size))
                self.add_unweighted_reservoir(triangle, times, res_size)
            else:
                if rnd.random() < 1.0*self.M / self.total_triangles:
                    random_triangle = rnd.randint(0,len(self.triangles) - 1)
                    triangle_to_be_deleted = self.triangles[random_triangle][0]
                    times_to_be_deleted = self.triangles[random_triangle][1]
                    time_deleted_triangle = self.triangles[random_triangle][2]
                    a = triangle_to_be_deleted[0]
                    b = triangle_to_be_deleted[1]
                    c = triangle_to_be_deleted[2]
                    tab = times_to_be_deleted[0]
                    tac = times_to_be_deleted[1]
                    tbc = times_to_be_deleted[2]
                    self.triangles[random_triangle]= (triangle,times,res_size)
                    self.delete_unweighted_reservoir( a, b, c, tab, tac, tbc, time_deleted_triangle)
                    self.add_unweighted_reservoir(triangle, times, res_size)
            self.total_triangles += 1
        else: #extra res is active
            if self.total_triangles_extra < self.M_extra:
                self.extra.append((triangle,times, res_size))
                self.add_unweighted_reservoir(triangle, times, res_size)
                self.total_triangles_extra += 1
            else:
                if self.merge_res():
                    if rnd.random() < 1.0*self.M / self.total_triangles:
                        random_triangle = rnd.randint(0,len(self.triangles) - 1)
                        triangle_to_be_deleted = self.triangles[random_triangle][0]
                        times_to_be_deleted = self.triangles[random_triangle][1]
                        time_deleted_triangle = self.triangles[random_triangle][2]
                        a = triangle_to_be_deleted[0]
                        b = triangle_to_be_deleted[1]
                        c = triangle_to_be_deleted[2]
                        tab = times_to_be_deleted[0]
                        tac = times_to_be_deleted[1]
                        tbc = times_to_be_deleted[2]
                        self.triangles[random_triangle]= (triangle,times,res_size)
                        self.delete_unweighted_reservoir( a, b, c, tab, tac, tbc, time_deleted_triangle)
                        self.add_unweighted_reservoir(triangle, times, res_size)
                    self.total_triangles += 1
                else:
                    if rnd.random() < 1.0*self.M_extra / self.total_triangles_extra:
                        random_triangle = rnd.randint(0,len(self.extra) - 1)
                        triangle_to_be_deleted = self.extra[random_triangle][0]
                        times_to_be_deleted = self.extra[random_triangle][1]
                        time_deleted_triangle = self.extra[random_triangle][2]
                        a = triangle_to_be_deleted[0]
                        b = triangle_to_be_deleted[1]
                        c = triangle_to_be_deleted[2]
                        tab = times_to_be_deleted[0]
                        tac = times_to_be_deleted[1]
                        tbc = times_to_be_deleted[2]
                        self.extra[random_triangle]= (triangle,times,res_size)
                        self.delete_unweighted_reservoir( a, b, c, tab, tac, tbc, time_deleted_triangle)
                        self.add_unweighted_reservoir(triangle, times, res_size)
                    self.total_triangles_extra += 1
    def merge_res(self):
        if (1.0*self.M/self.total_triangles) > (1.0*self.M_extra/(self.total_triangles_extra + 1)):
            p1 = 1.0*self.M/self.total_triangles
            p2 = 1.0*self.M_extra/self.total_triangles
            for triangle in self.extra:
                if rnd.random() < p1/p2:
                    self.triangles.append(triangle)
                    self.total_triangles += 1
                    self.M += 1
                else:
                    triangle_to_be_deleted = triangle[0]
                    times_to_be_deleted = triangle[1]
                    time_deleted_triangle = triangle[2]
                    a = triangle_to_be_deleted[0]
                    b = triangle_to_be_deleted[1]
                    c = triangle_to_be_deleted[2]
                    tab = times_to_be_deleted[0]
                    tac = times_to_be_deleted[1]
                    tbc = times_to_be_deleted[2]
                    self.delete_unweighted_reservoir(a, b, c, tab, tac, tbc, time_deleted_triangle)
            self.extra = []
            self.total_triangles_extra = 0
            self.M_extra = 0
            self.active_res = 1
            return True
        return False


    def update_cliques(self, u, v, edge_reservoir):

        is_u = u in self.unweighted_reservoir
        is_v = v in self.unweighted_reservoir
        if is_u and is_v:
            triangles_u = self.unweighted_reservoir[u]
            triangles_v = self.unweighted_reservoir[v]
            for tr_u in triangles_u:
                for tr_v in triangles_v:

                    if tr_u[0] == tr_v[0] and tr_u[2]== tr_v[2]:
                        t1 = tr_u[4]
                        t2 = tr_u[1]
                        t4 = tr_u[3]
                        t3 = tr_v[3]
                        t5 = tr_v[1]
                      
                        self.cliques_seen += 1
                        p = self.cliques_probability(t1, t2, t3, t4, t5, tr_u[-1], tr_v[-1]) # update the probabilities

                        self.cliques += 1.0/p


    def cliques_probability(self,  t1,  t2,  t3,  t4, t5, tr1_res, tr2_res): #update this module
        max1 = max(t2, t4)
        min1 = min(t2, t4)
        max2 = max(t3, t5)
        min2 = min(t3, t5)
        p1 = 0
        if self.active_res == 1:
            p11 = min(1.0, 1.0*(self.M - 1)/(self.total_triangles - 1))
            p2 = min(1.0, (1.0*self.M/self.total_triangles)) * min(1.0, 1.0*tr2_res/(max(t1, max2)-1)) * min(1.0, 1.0*(tr2_res - 1)/(max(t1,max2) - 2))
        else:
            p11 = min(1.0, 1.0*(self.M_extra - 1)/(self.total_triangles_extra - 1))
            p2 = min(1.0, (1.0*self.M_extra/self.total_triangles_extra)) * min(1.0, 1.0*tr2_res/(max(t1, max2)-1)) * min(1.0, 1.0*(tr2_res - 1)/(max(t1,max2) - 2))
        if t1 > max(t2, t3, t4, t5):
            p1 = min(1.0, (tr1_res - 3.0)/(t1 - 4)) * min(1.0, 1.0*(tr1_res - 2)/(t1 - 3))
        elif max2 > t1 > max(max1, min1, min2):
            p1 = min(1.0, (tr1_res - 2.0)/(t1 - 3)) * min(1.0, 1.0*(tr1_res - 1)/(t1 - 2))
        elif max2 > max1 > max(min1, min2, t1):
            p1 = min(1.0, (tr1_res - 2.0)/(max1 - 3))
        elif max2 > min2 > t1 > max(max1, min1):
            p1 = min(1.0, (tr1_res - 1.0)/(t1 - 2)) * min(1.0, 1.0*(tr1_res)/(t1 - 1))
        elif max2 > min2 > max1 > max(t1, min1):
            p1  = min(1.0, (tr1_res - 1.0)/(max1 - 2))
        elif max1 > t1 > max(min1, max2, min2):
            p1 = min(1.0, (tr1_res - 1.0)/(max1 - 2)) * min(1.0, (tr1_res - 2.0)/(t1 - 3)) * min(1.0, 1.0*max(self.memory, t1 - 1)/(max1 - 1))
        elif max1 > max2 > max(t1, min1, min2):
            p1 = min(1.0, 1.0*max(self.memory, max2 - 2)/(max1 - 2)) *min(1.0, 1.0*max(self.memory, max2 - 1)/(max1 - 1)) * min(1.0, (tr2_res - 2.0)/(max2 - 3))
        elif max1 > min1 > t1 > max2 > min2: #maybe change this
            p1 = min(1.0, (tr1_res - 1.0)/(max1 - 2)) * min(1.0, 1.0*(tr1_res)/(max1 - 1))
        else:
            p1 = min(1.0, (tr1_res - 1.0)/(max1 - 2)) * min(1.0, 1.0*max(self.memory,max2 - 1)/(max1 - 2))
        # print p1, p11, p2
        return p1*p11*p2

    def update_triangles(self, u, v, res_size):
        common_neighbors = self.graph.get_common_neighbors(u,v)

        for x in common_neighbors:
            self.edge_reservoir.total_triangles += 1
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
            self.sample_triangle(tuple(triangle), times, res_size )
    def get_number_squares(self):
        return self.cliques






