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
    parser.add_argument('-t', metavar='type', type=int, help='1 - Squares from edges, 2 - Squares from wedges')
    args = parser.parse_args()
    graph_file = args.g
    res_size = args.r
    seed = args.s if args.s else 42
    type = args.t if args.t else 10000
    
    graph = Graph.Graph()
    edge_reservoir = Edge_Reservoir.EdgeReservoir(res_size, graph)
    wedge_reservoir = Reservoir.WedgeReservoir(type,graph, edge_reservoir)
    file_graph = open(graph_file, 'r')
    cnt = 1
    cliques_seen = 0
    cliques=0
    start = time.time()
    print 'Edges','Single_Res'
    for line in file_graph:
        if cnt%10000==0:
            print cnt,cliques
        cnt+=1
        elements = line.split(" ")
        u = int(elements[0])
        v = int(elements[1])
        edge_reservoir.total_edges += 1
        c = 0
        if u in graph.graph_structure and v in graph.graph_structure:
            common_neighbors = graph.get_common_neighbors(u,v)
            if len(common_neighbors) >= 3:
                for x,y,z in itertools.combinations(common_neighbors,3):
                    if x in graph.graph_structure[y] and y in graph.graph_structure[z] and z in graph.graph_structure[x]:
                        c += 1
                        # print 'Found'
                        cliques_seen += 1
                if edge_reservoir.total_edges<=9:
                    p = 1
                else:
                    p = min(1.0, 1.0*edge_reservoir.M/(edge_reservoir.total_edges-1))\
                        *min(1.0, (1.0*edge_reservoir.M-1)/(edge_reservoir.total_edges-2))\
                        *min(1.0, 1.0*(edge_reservoir.M-2)/(edge_reservoir.total_edges-3))\
                        *min(1.0, 1.0*(edge_reservoir.M-3)/(edge_reservoir.total_edges-4))\
                        *min(1.0, 1.0*(edge_reservoir.M-4)/(edge_reservoir.total_edges-5))\
                        *min(1.0, 1.0*(edge_reservoir.M-5)/(edge_reservoir.total_edges-6))\
                        *min(1.0, 1.0*(edge_reservoir.M-6)/(edge_reservoir.total_edges-7))\
                        *min(1.0, 1.0*(edge_reservoir.M-7)/(edge_reservoir.total_edges-8))\
                        *min(1.0, 1.0*(edge_reservoir.M-8)/(edge_reservoir.total_edges-9))

                p_clique = max(1.0, 1.0/p)
                cliques+= p_clique*c

        edge_reservoir.sample_edge(u,v, edge_reservoir.total_edges)
    print "#",time.time() - start
if __name__ == '__main__':
    main()

