__author__ = 'erisa'
import argparse
import Graph
import Reservoir
import Edge_Reservoir as Edge_Reservoir
import time
import itertools

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', metavar='graph', required=True, type=str, help='graph file')
    parser.add_argument('-r', metavar='size', required=True, type=int, help='reservoir size')
    parser.add_argument('-s', metavar='seed', type=int, help='random seed')

    args = parser.parse_args()
    graph_file = args.g
    res_size = args.r
    seed = args.s if args.s else 42
    
    graph = Graph.Graph()
    edge_reservoir = Edge_Reservoir.EdgeReservoir(res_size, graph)
    wedge_reservoir = Reservoir.WedgeReservoir(type,graph, edge_reservoir)
    file_graph = open(graph_file, 'r')
    cnt = 1
    cliques_seen = 0
    cliques=0
    
    start = time.time()
    
    print 'Edges','Cliques'
    
    for line in file_graph:
        if cnt%10000==0:
            print cnt,cliques
        cnt+=1
        elements = line.split(" ")
        try:
	    u = int(elements[0])
            v = int(elements[1])
	except:
	    u = int(elements[1])
            v = int(elements[2])
        edge_reservoir.total_edges += 1
        c = 0
        if u in graph.graph_structure and v in graph.graph_structure:
            common_neighbors = graph.get_common_neighbors(u,v)
            for a,b in itertools.combinations(common_neighbors,2):
                if a != b and b in graph.graph_structure[a]:
                    c += 1
                    cliques_seen += 1
            if edge_reservoir.total_edges <= 5:
                p = 1
            else:
                p = min(1.0, 1.0*edge_reservoir.M/(edge_reservoir.total_edges-1))\
                    *min(1.0, (1.0*edge_reservoir.M-1)/(edge_reservoir.total_edges-2))\
                    *min(1.0, 1.0*(edge_reservoir.M-2)/(edge_reservoir.total_edges-3))\
                    *min(1.0, 1.0*(edge_reservoir.M-3)/(edge_reservoir.total_edges-4))\
                    *min(1.0, 1.0*(edge_reservoir.M-4)/(edge_reservoir.total_edges-5))
            p_clique = max(1.0, 1.0/p)
            cliques+= p_clique*c

        edge_reservoir.sample_edge(u,v, edge_reservoir.total_edges)

    print "#",time.time() - start
if __name__ == '__main__':
    main()

