# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:28:56 2017

@author: guilaume
"""

import networkx as nx
import xml.etree.ElementTree as ET
import Bipartite as bp
from load_gxl import create_graph_from_gxl
from functions import A_star
import glob
import random
import pickle
import os
import time
import sys
import math
import numpy as np


def create_base_app(path, number_of_file_for_app):
    t = time.time()
    liste_gxl = glob.glob(path)
    if number_of_file_for_app > len(liste_gxl):
        print "Number of files for app larger than number of files. Selecting the whole base for app"
        number_of_file_for_app = len(liste_gxl)
    liste_app = random.sample(liste_gxl, number_of_file_for_app)
    liste_tuple = []
    for i in range(len(liste_app)):
        for j in range(i,len(liste_app)):
            print os.path.basename(liste_app[i]),os.path.basename(liste_app[j])
            G1 = create_graph_from_gxl(liste_app[i])
            G2 = create_graph_from_gxl(liste_app[j])
            
            true_ged = A_star(G1,G2)
            permuted_matrix,cost = bp.create_matrix_and_permute_it(G1,G2)
            print cost, true_ged[-1][-1]
            permuted_matrix = np.expand_dims(permuted_matrix, axis=-1)
            permuted_matrix[permuted_matrix == float('inf')] = 10
            #permuted_matrix[permuted_matrix == float('inf')] = np.amax(permuted_matrix[permuted_matrix != float('inf')])
            #print permuted_matrix
            liste_tuple.append((permuted_matrix,true_ged[-1][-1],cost))
    print "True GED et permuted matrix créée. Temps écoulé : ", time.time()-t
    random.shuffle(liste_tuple)
    liste_app = liste_tuple[:int(math.floor(3*len(liste_tuple)/5))]
    liste_valid = liste_tuple[int(math.floor(3*len(liste_tuple)/5)):int(math.floor(4*len(liste_tuple)/5))]
    liste_test = liste_tuple[int(math.floor(4*len(liste_tuple)/5)):]
    print len(liste_tuple),len(liste_app),len(liste_valid), len(liste_test)
    with open("base_app.p","w+") as fp:
        pickle.dump(liste_app,fp)
    with open("base_valid.p","w+") as fp:
        pickle.dump(liste_valid,fp)
    with open("base_test.p","w+") as fp:
        pickle.dump(liste_test,fp)
        
    
    
            
        
if __name__ == "__main__":
    path_to_gxl = "../Datasets/Letter/LOW/*.gxl"
    create_base_app(path_to_gxl,60)
    with open("base_app.p","r") as fp:
        app=pickle.load(fp)
    with open("base_valid.p","r") as fp:
        valid = pickle.load(fp)
    with open("base_test.p","r") as fp:
        test = pickle.load(fp)
        
    print len(app), len(valid),len(test)