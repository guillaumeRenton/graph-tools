#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:55:51 2017

@author: renton
"""

from model import creerModel
import pickle
import numpy as np
from Bipartite import calcul_cost_permuted, calcul_Munkres
import time


def predict(path, weights):
    
    with open(path+"base_test.p","r") as fp:
        basetest = pickle.Unpickler(fp).load()
    
    print (len(basetest))
    model = creerModel(weights)
    Mse_bp_ged = 0
    Mse_model = 0
    
    for test in basetest : 
        batch= np.expand_dims(test[0], axis=0)
        value_approx = model.predict(batch)
        C_star = test[0].squeeze()
        C_star[C_star ==10] = float('inf')
        cost,h = calcul_Munkres(C_star)
        print h
        Mse_bp_ged += (cost - test[1])**2
        Mse_model += (value_approx-test[1])**2
        print test[1], cost, value_approx
    Mse_bp_ged = Mse_bp_ged/len(basetest)
    Mse_model = Mse_model/len(basetest)
    

    print("Mse BP GED : ", Mse_bp_ged)
    print("Mse modele : ", Mse_model)
    
if __name__ == "__main__":
    t=time.time()
    predict("", "weights/model_test1_70.h5")
    print("Temps ecoule : ", time.time()-t)