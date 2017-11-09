# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:44:11 2017

@author: guilaume
"""

import pickle

from Bipartite import calcul_Munkres

if __name__ == "__main__":
    with open("base_app.p","r") as fp:
        app=pickle.load(fp)
    with open("base_valid.p","r") as fp:
        valid = pickle.load(fp)
    
    MSE = 0
    for fileapp in app:
        MSE += (fileapp[2]- fileapp[1])**2
    print MSE/len(app)
      
    MSE = 0
    for filevalid in valid:
        MSE += (filevalid[2]- filevalid[1])**2
    print MSE/len(valid)
        