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
    parser.add_argument('-t', metavar='type', type=int, help='triangle reservoir size')
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
    
    start = time.time()
    
    print 'Edges','Triangles_Seen','Triangle_Estimation','Clique_Seen_1Reservoir','Cliques_Seen_2Reservoir','Cliques_Estimation_1Res','Cliques_Estimation_2Res'

    for line in file_graph:
        if cnt%10000==0:
            print cnt,wedge_reservoir.total_triangles,wedge_reservoir.triangle_estimator,cliques_seen,wedge_reservoir.cliques_seen,wedge_reservoir.fourest_estimator,wedge_reservoir.get_number_squares()
        cnt+=1
        elements = line.split(" ")
        u = int(elements[0])
        v = int(elements[1])
        edge_reservoir.total_edges += 1
        c = 0
        if u in graph.graph_structure and v in graph.graph_structure:
            common_neighbors = graph.get_common_neighbors(u,v)
            for a,b in itertools.combinations(common_neighbors,2):
                    if a != b and b in graph.graph_structure[a]:
                        c += 1
                        cliques_seen += 1
            if edge_reservoir.total_edges<=5:
                p = 1
            else:
                p = min(1.0, 1.0*edge_reservoir.M/(edge_reservoir.total_edges-1))\
                    *min(1.0, (1.0*edge_reservoir.M-1)/(edge_reservoir.total_edges-2))\
                    *min(1.0, 1.0*(edge_reservoir.M-2)/(edge_reservoir.total_edges-3))\
                    *min(1.0, 1.0*(edge_reservoir.M-3)/(edge_reservoir.total_edges-4))\
                    *min(1.0, 1.0*(edge_reservoir.M-4)/(edge_reservoir.total_edges-5))
            p_clique = max(1.0, 1.0/p)
            wedge_reservoir.fourest_estimator+= p_clique*c
            p = min(1.0, 1.0*edge_reservoir.M/(edge_reservoir.total_edges-1))\
                *min(1.0, 1.0*(edge_reservoir.M-1)/(edge_reservoir.total_edges-2))
            p_triangle = max(1, 1.0/p)
            wedge_reservoir.triangle_estimator += len(common_neighbors)*p_triangle
        wedge_reservoir.update_cliques(u,v, edge_reservoir)
        wedge_reservoir.update_triangles(u, v)
        edge_reservoir.sample_edge(u,v, edge_reservoir.total_edges)
    print "#",time.time() - start
if __name__ == '__main__':
    main()

