# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:55:43 2017

@author: guilaume
"""

import networkx as nx
from scipy.optimize import linear_sum_assignment
import numpy as np
from functions import calcul_distance_node,calcul_distance_edge, A_star
from load_gxl import create_graph_from_gxl
import matplotlib.pyplot as plt

def calcul_cost_edge(edges_source,edges_target):
    n = len(edges_source)
    m = len(edges_target)
    
    C_star = np.full((n+m,n+m), float('inf'))   
    
    for i in range(n+m):
        for j in range(n+m):
            if i<len(edges_source) and j<len(edges_target):
                edge_1 = edges_source[edges_source.keys()[i]]
                edge_2 = edges_target[edges_target.keys()[j]]
                C_star[i][j]= calcul_distance_edge(edge_1,edge_2)
            elif i < len(edges_source) and j == m+i:
                C_star[i][j]=1
            elif j < len(edges_target) and i == n+j:
                C_star[i][j]=1
            elif i >= len(edges_source) and j >= len(edges_target):
                C_star[i][j]=0
    hungarian = linear_sum_assignment(C_star)
    total_cost=0
    for i in range(len(hungarian[0])):
        total_cost = total_cost+C_star[hungarian[0][i]][hungarian[1][i]]
    return total_cost


def create_cost_matrix(graph_source, graph_target):
    n = len(graph_source.nodes)
    m = len(graph_target.nodes)
    
    C_star_node = np.full((n+m,n+m), float('inf'))
    C_star_edge = np.full((n+m,n+m), float(0))
    
    for i in range(n+m):
        for j in range(n+m):
            if i<len(graph_source.nodes) and j<len(graph_target.nodes):
                C_star_node[i][j]=calcul_distance_node(graph_source.node[list(graph_source.nodes)[i]], graph_target.node[list(graph_target.nodes)[j]])
                C_star_edge[i][j]=calcul_cost_edge(graph_source[list(graph_source.nodes)[i]], graph_target[list(graph_target.nodes)[j]])
            elif i < len(graph_source.nodes) and j == m+i:
                C_star_node[i][j]=1
                C_star_edge[i][j]=len(graph_source[list(graph_source.nodes)[i]])
            elif j < len(graph_target.nodes) and i == n+j:
                C_star_node[i][j]=1
                C_star_edge[i][j]=len(graph_target[list(graph_target.nodes)[j]])
            elif i >= len(graph_source.nodes) and j >= len(graph_target.nodes):
                C_star_node[i][j]=0
    C_star = C_star_node+C_star_edge
    return C_star_node,C_star
 

def calcul_adjacency_extended(graph_source, graph_target):
    n = len(graph_source.nodes)
    m = len(graph_target.nodes)
    adjacency_source = np.full((n+m,n+m), float(0))
    adjacency_target = np.full((n+m,n+m), float(0))
    for i in range(n+m):
        for j in range(n+m):
            if i<len(graph_source.nodes) and j<len(graph_source.nodes):
                node_source_1 = list(graph_source.nodes)[i]
                node_source_2 = list(graph_source.nodes)[j]
                edge_source_1=(node_source_1,node_source_2)
                edge_source_2=(node_source_2,node_source_1)
                if edge_source_1 in graph_source.edges or edge_source_2 in graph_source.edges:
                    adjacency_source[i][j]=1
            if i<len(graph_target.nodes) and j<len(graph_target.nodes):
                node_target_1 = list(graph_target.nodes)[i]
                node_target_2 = list(graph_target.nodes)[j]
                edge_target_1=(node_target_1,node_target_2)
                edge_target_2=(node_target_2,node_target_1)
                
                if edge_target_1 in graph_target.edges or edge_target_2 in graph_target.edges:
                    adjacency_target[i][j]=1
    return adjacency_source, adjacency_target
            
  
def calcul_Munkres(graph_source,graph_target,C_nodes,C_star):
    hungarian = linear_sum_assignment(C_star)
    total_cost=0
    adjacency_source,adjacency_target = calcul_adjacency_extended(graph_source,graph_target)
    for i in range(len(hungarian[0])):
        total_cost+= C_nodes[hungarian[0][i]][hungarian[1][i]]
    
    for i in range(len(hungarian[0])):
        for j in range(i+1,len(hungarian[0])):
            total_cost+=abs(adjacency_source[i][j]-adjacency_target[hungarian[1][i]][hungarian[1][j]])
    return total_cost, hungarian
        
    
def create_matrix_and_permute_it(graph_source, graph_target):
    C_node,C_star = create_cost_matrix(graph_source, graph_target)
    cost, permutation = calcul_Munkres(graph_source,graph_target,C_node,C_star)
    C_star_permute = C_star[:,permutation[1]]
    return C_star_permute, cost
    

if __name__ == "__main__":
    
    G1 = nx.Graph()
    G1.add_node("u1")
    G1.add_node("u2")
    G1.add_node("u3")
    G1.add_node("u4")
    G1.node["u1"]["x"]=1
#    G1.node["u1"]["y"]=2
    G1.node["u2"]["x"]=2
#    G1.node["u2"]["y"]=2
    G1.node["u3"]["x"]=1
#    G1.node["u3"]["y"]=2
    G1.node["u4"]["x"]=3
#    G1.node["u4"]["y"]=2
    G1.add_edges_from([("u1","u2"),("u2","u3"),("u2","u4"),("u3","u4")])
#    G1.add_edges_from([("u1","u2",{"x":1}),("u2","u3",{"x":0.65}),("u2","u4",{"x":1}),("u3","u4",{"x":0.5})])

    
    G2 = nx.Graph()
    
    G2.add_node("v1")
    G2.add_node("v2")
    G2.add_node("v3")
    G2.node["v1"]["x"]=3
#    G2.node["v1"]["y"]=3
    G2.node["v2"]["x"]=2
#    G2.node["v2"]["y"]=2
    G2.node["v3"]["x"]=2
#    G2.node["v3"]["y"]=1
    G2.add_edges_from([("v1","v2"),("v2","v3")])    
#    G2.add_edges_from([("v1","v2",{"x":0.65}),("v2","v3",{"x":0.5})])    
    c_node, c_star = create_cost_matrix(G1,G2)
#   
    print calcul_Munkres(G1,G2,c_node,c_star)
    
    graph1 = create_graph_from_gxl("../Datasets/Letter/LOW/YP1_0008.gxl")
    graph2 = create_graph_from_gxl("../Datasets/Letter/LOW/XP1_0114.gxl")
    
    c_node, c_star = create_cost_matrix(graph1,graph2)
#   
    print calcul_Munkres(graph1,graph2,c_node,c_star)
    
#    nx.draw_networkx(graph1, with_labels=True)
#    nx.draw_networkx(graph2, with_labels=True,node_color = 'b')
#    plt.show()
#    
#    print "Cost matrix"
#    print create_cost_matrix(graph1,graph2)
#    print "Munkres"
#    print calcul_Munkres(create_cost_matrix(graph1,graph2))
#    print "A star"
#    print A_star(graph1,graph2)
#    
#    print calcul_Munkres(create_cost_matrix(G2,G2))
#    
#    print calcul_Munkres(create_matrix_and_permute_it(G1,G2)[0])
