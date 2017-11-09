# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:42:26 2017

@author: guilaume
"""

import networkx as nx
import xml.etree.ElementTree as ET

def create_graph_from_gxl(filename):
    tree = ET.parse(filename)
    graph = tree.find(".//graph")
    if graph.attrib["edgemode"]=="undirected":
        G = nx.Graph()
    elif graph.attrib["edgemode"]=="directed":
        G=nx.DiGraph()
    else:
        print "No edge mode specified, assuming undirected graph\n"
        G=nx.Graph()
    for node in tree.findall(".//node"):
        gid = node.attrib["id"]
        G.add_node(gid)
        for attr in node.findall(".//attr"): 
            G.node[gid][attr.attrib['name']]=attr[0].text

    for edge in tree.findall(".//edge"):
        G.add_edge(edge.attrib["from"],edge.attrib["to"])
    return G