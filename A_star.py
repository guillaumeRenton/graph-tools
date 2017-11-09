# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:39:14 2017

@author: guilaume
"""

import networkx as nx
from load_gxl import create_graph_from_gxl
import sys
import math
import time

def calcul_distance_edge(edge_source,edge_target):
    if not type(edge_source)==dict:
        return 0
    if not edge_source.keys() == edge_target.keys():
        print "Error : edgess attributes aren't the same\n edge 1 : ", edge1.keys(),"\n node 2 ",edge2.keys()
        sys.exit()
    
    d = 0
    
    for key in edge_source.keys():
        d+= (float(edge_source[key])-float(edge_target[key]))**2
    
    return math.sqrt(d)

def calcul_distance_node(node1,node2):
    if not node1.keys() == node2.keys():
        print "Error : nodes attributes aren't the same\n node 1 : ", node1.keys(),"\n node 2 ",node2.keys()
        sys.exit()
    
    d = 0
    
    for key in node1.keys():
        d+= (float(node1[key])-float(node2[key]))**2
    
    return math.sqrt(d)
    

def A_star(graph_source, graph_target):
    OPEN = []
    liste_node_source = list(graph_source.nodes)
    for node in graph_target.nodes:
        tmp = calcul_distance_node(graph_source.node[liste_node_source[0]],graph_target.node[node])
        OPEN.append([(liste_node_source[0], node, tmp)])
    OPEN.append([(liste_node_source[0],"eps",1.0)])

    complete = set(graph_target.nodes)
    
    while(1):
        p = OPEN.index(min(OPEN, key=lambda t:t[-1][2]))
        liste_node = set(item[1] for item in OPEN[p])
        lambda_min = list(OPEN[p])
        if complete.issubset(liste_node) and len(lambda_min) >= len(liste_node_source):
            return OPEN[p]
        
        OPEN.remove(lambda_min)
        
        if len(lambda_min) < len(liste_node_source):
            for node_target in graph_target.nodes:
                if node_target not in liste_node:
                    cost = lambda_min[-1][-1] + calcul_distance_node(graph_source.node[liste_node_source[len(lambda_min)]],graph_target.node[node_target])

                    for matching in lambda_min:
                        edge_source_1 = (liste_node_source[len(lambda_min)],matching[0])
                        edge_source_2 = (matching[0],liste_node_source[len(lambda_min)])
                        edge_target_1 = (node_target, matching[1])
                        edge_target_2 = (matching[1],node_target)

                        if (edge_source_1 in graph_source.edges or edge_source_2 in graph_source.edges) and (edge_target_1 in graph_target.edges or edge_target_2 in graph_target.edges):
                            edge_source = edge_source_1 if edge_source_1 in graph_source.edges else edge_source_2
                            edge_target = edge_target_1 if edge_target_1 in graph_target.edges else edge_target_2
                            cost += calcul_distance_edge(edge_source, edge_target)
                        elif edge_source_1 not in graph_source.edges and edge_source_2 not in graph_source.edges and edge_target_1 not in graph_target.edges and edge_target_2 not in graph_target.edges:
                            cost += 0
                        else :
                            cost += 1

                    lambda_tmp = list(lambda_min)
                    lambda_tmp.append((liste_node_source[len(lambda_min)], node_target, cost))
                    OPEN.append(lambda_tmp)
            
            lambda_tmp = list(lambda_min)
            cost = lambda_min[-1][2]+1
            for matching in lambda_min:
                edge_source_1 = (liste_node_source[len(lambda_min)],matching[0])
                edge_source_2 = (matching[0],liste_node_source[len(lambda_min)])
                if edge_source_1 in graph_source.edges or edge_source_2 in graph_source.edges:
                    cost +=1
            lambda_tmp.append((liste_node_source[len(lambda_min)], "eps", cost))
            OPEN.append(lambda_tmp)
        else:
            for node_target in graph_target.nodes:
                if node_target not in liste_node:
                    lambda_tmp = list(lambda_min)
                    cost = lambda_min[-1][2]+1
                    for matching in lambda_min:
                        edge_target_1 = (node_target, matching[1])
                        edge_target_2 = (matching[1],node_target)
                        if edge_target_1 in graph_target.edges or edge_target_2 in graph_target.edges:
                            cost += 1
                    lambda_tmp.append(("eps",node_target, cost))
                    OPEN.append(lambda_tmp)
                    
                    
            

            
        
        

        
        
if __name__ == "__main__":
    graph1 = create_graph_from_gxl("../Datasets/Letter/LOW/AP1_0000.gxl")
    graph2 = create_graph_from_gxl("../Datasets/Letter/LOW/AP1_0001.gxl")
    
    
    G1 = nx.Graph()
    G1.add_node("u1", weight=1)
    G1.add_node("u2", weight=2)
    G1.add_node("u3", weight=1)
    G1.add_node("u4", weight=3)
    
    G1.add_edges_from([("u1","u2"),("u2","u3"),("u2","u4"),("u3","u4")])

    
    G2 = nx.Graph()
    
    G2.add_node("v1", weight=3)
    G2.add_node("v2", weight=2)
    G2.add_node("v3", weight=2)
    
    G2.add_edges_from([("v1","v2"),("v2","v3")])
    
    t=time.time()
    A_star(G1,G2)
    print "temps écoulé :", time.time()-t
    t=time.time()
    A_star(G2,G1)
    print "Temps écoulé :", time.time()-t
    t = time.time()
    A_star(G2,G2)
    print "temps écoulé :", time.time()-t

    A_star(graph1, graph2)