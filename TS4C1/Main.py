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
    start = time.time()

    print 'Edges','Triangles_Seen','Triangle_Estimation','Clique_Seen_1Reservoir','Cliques_Seen_2Reservoir','Cliques_Estimation_1Res','Cliques_Estimation_2Res'

    for line in file_graph:
        if cnt%10000==0:
            print cnt,wedge_reservoir.total_triangles,wedge_reservoir.triangle_estimator,len(wedge_reservoir.seen),wedge_reservoir.cliques_seen,wedge_reservoir.fourest_estimator,wedge_reservoir.get_number_squares()
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
        wedge_reservoir.update_cliques(u,v, edge_reservoir)
        wedge_reservoir.update_triangles(u, v)
        edge_reservoir.sample_edge(u,v, edge_reservoir.total_edges)
   
    print "#",time.time() - start
if __name__ == '__main__':
    main()

