__author__ = 'erisa'
#import numpy as np
class Graph:
    def __init__(self):
        self.num_nodes = 0
        self.num_edges = 0
        self.graph_structure = {}

    def add_edge(self, source, destination, t):
        assert source != destination
        assert source >= 0
        assert destination >= 0

        s = True if source in self.graph_structure else False
        d = True if destination in self.graph_structure else False
        d_in_s = True if s and destination in self.graph_structure[source] else False
        if not s:
            self.num_nodes+=1

        if not d:
            self.num_nodes+=1

        if s and d_in_s:
            return False

        self.num_edges += 1

        if s: self.graph_structure[source][destination] = t
        else: self.graph_structure[source] = {destination:t}
        if d: self.graph_structure[destination][source] = t
        else: self.graph_structure[destination] = {source:t}

        return True


    def remove_edge(self, source, destination):
        if source in self.graph_structure:
            if not (destination in self.graph_structure[source]):
                return False
        else:
            return False # edge not found

        self.num_edges -= 1

        if len(self.graph_structure[source]) == 1:
            del self.graph_structure[source]
            self.num_nodes -= 1
        else:
            del self.graph_structure[source][destination]

        if len(self.graph_structure[destination]) == 1:
            del self.graph_structure[destination]
            self.num_nodes -= 1
        else:
            del self.graph_structure[destination][source]

        return True

    def reset_graph(self):
        self.num_nodes = 0
        self.num_edges = 0
        self.graph_structure = {}

    def get_num_nodes(self):
        return self.num_nodes

    def get_num_edges(self):
        return self.num_edges


    def get_degree(self, source):
        if source in self.graph_structure:
            return len(self.graph_structure[source])
        else:
            return 0
    def get_edges(self):
        return self.graph_structure

    def get_neighbors(self, source):
        if source in self.graph_structure:
            return self.graph_structure[source]
        else:
            return []

    def get_common_neighbors(self, u, v):
        neighbors_u = self.get_neighbors(u)
        neighbors_v = self.get_neighbors(v)
        deg_u = len(neighbors_u)
        deg_v = len(neighbors_v)
        if deg_u > deg_v:
            return set(neighbors_v).intersection(set(neighbors_u))
        else:
            return set(neighbors_u).intersection(set(neighbors_v))


    def get_union_neighbors(self, u, v):
        s = True if u in self.graph_structure else False
        d = True if v in self.graph_structure else False
        res = []
        if s and d:
            n_u = self.get_neighbors(u)
            nr_n_u = len(n_u)
            n_v = self.get_neighbors(v)
            nr_n_v = len(n_v)
            res.extend([(v,neighbor, u) for neighbor in n_u])
            res.extend([(u,neighbor,v) for neighbor in n_v])
        elif s:
            return [(v,neighbor, u) for neighbor in self.get_neighbors(u) if neighbor != v]
        elif d:
            return [(u,neighbor,v) for neighbor in self.get_neighbors(v) if neighbor != u]
        return res



