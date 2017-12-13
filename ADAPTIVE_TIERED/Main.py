__author__ = 'erisa'
import argparse
import Graph
import Reservoir
import Edge_Reservoir as Edge_Reservoir
import time
import math
import itertools
from helping_functions import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', metavar='graph', required=True, type=str, help='graph file')
    parser.add_argument('-r', metavar='size', required=True, type=int, help='reservoir size')
    parser.add_argument('-s', metavar='seed', type=int, help='random seed')
    parser.add_argument('-t', metavar='type', type=int, help='1 - Squares from edges, 2 - Squares from wedges')
    args = parser.parse_args()
    graph_file = args.g
    res_size = args.r
	
    graph = Graph.Graph()
    edge_reservoir = Edge_Reservoir.EdgeReservoir(res_size, graph, res_size)
	
    file_graph = open(graph_file, 'r')
    cnt = 1
    old_total = 0
    switched = False
    start = time.time()
    old_alpha = 0
    for line in file_graph:
        if cnt%10000==0:
            if switched:
                print cnt,edge_reservoir.total_triangles,edge_reservoir.M, wedge_reservoir.M, wedge_reservoir.cliques_seen, wedge_reservoir.cliques, "T"
            else:
                print cnt,edge_reservoir.total_triangles, edge_reservoir.M, 0, edge_reservoir.cliques_seen, edge_reservoir.cliques, "E"

	
        if cnt % res_size == 0: #check whether to change the spaces or not
            cliques_seen_last_block  = edge_reservoir.total_triangles - old_total

            old_total = edge_reservoir.total_triangles
            if not switched:
                triangle_density = 1.0 * (edge_reservoir.total_triangles + cliques_seen_last_block) / edge_reservoir.M
                if triangle_density > 1.0/3:
                    alpha = 1.0/3
                    old_alpha = 1.0/3
                else:
                    alpha = triangle_density
                    old_alpha = triangle_density
                if check_condition(edge_reservoir.M, cnt + edge_reservoir.M, alpha, edge_reservoir.total_triangles + cliques_seen_last_block) == 2: # first time to create the triangle reservoir
                    deleted = edge_reservoir.shrinkByAlpha(alpha)
                    
                    wedge_reservoir = Reservoir.WedgeReservoir(deleted,graph, edge_reservoir, edge_reservoir.cliques, res_size) #create the triangle reservoirf
                    for triangle in edge_reservoir.triangles_seen[0:wedge_reservoir.M]:
                        wedge_reservoir.sample_triangle(triangle[0], triangle[1], res_size)
                        wedge_reservoir.total_triangles += 1
                    switched = True
            else:
                triangle_density = 1.0 * (edge_reservoir.total_triangles + cliques_seen_last_block) / edge_reservoir.M
                if triangle_density > 1.0/3:
                    alpha = 1.0/3
                else:
                    alpha = triangle_density
                if alpha > old_alpha and wedge_reservoir.active_res == 1: # if we need more space and extra space is empty
                    deleted = edge_reservoir.shrinkByAlpha(alpha - old_alpha)
                    wedge_reservoir.active_res = 2
                    wedge_reservoir.M_extra = deleted
                old_alpha = alpha
            # print cnt, edge_reservoir.M, wedge_reservoir.M, wedge_reservoir.M_extra, len(wedge_reservoir.triangles), len(wedge_reservoir.extra),wedge_reservoir.total_triangles, wedge_reservoir.total_triangles_extra
        cnt+=1
        elements = line.split(" ")
        try:
            u = int(elements[0])
            v = int(elements[1])
        except:
            u = int(elements[1])
            v = int(elements[2])
        edge_reservoir.total_edges += 1
        if switched:
            wedge_reservoir.update_cliques(u,v, cnt)
            wedge_reservoir.update_triangles(u,v, edge_reservoir.M)
        else:
            edge_reservoir.update_cliques(u,v, cnt)
            edge_reservoir.update_triangles(u, v, cnt,res_size)
        edge_reservoir.sample_edge(u,v, cnt)

    # print (1.0*res_size/edge_reservoir.total_edges)**5
    # print ((res_size - alpha * res_size)/edge_reservoir.total_edges)**4 * ((alpha * res_size)/edge_reservoir.total_triangles)**2
    print "#",time.time() - start
if __name__ == '__main__':
    main()

