# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 17:15:26 2017

@author: guilaume
"""

from keras.models import Model,Sequential
from keras.optimizers import SGD, Adam
from keras.layers import Flatten, Dense, Dropout, Reshape, Permute, Activation, \
    Input, merge,  MaxPooling2D, Conv2DTranspose, UpSampling2D
from keras.utils import np_utils
from keras.layers.convolutional import Convolution2D
import keras.backend as K
from keras.initializers import Constant
from spp.SpatialPyramidPooling import SpatialPyramidPooling
from keras.callbacks import TensorBoard
import pickle
import random
import numpy as np

def creerModel(weights_path=None):
    """
    Model creation.
    nbClasses is the number of classes for the last layer
    Weights_path is for either prediction or transfer learning
    """
    model = Sequential()
    model.add(Convolution2D(64, (3,3), activation='relu',padding='same', dilation_rate=(1, 1), input_shape=(None,None,1)))
    model.add(Convolution2D(64, (3,3), activation='relu',padding='same', dilation_rate=(1, 1)))

    model.add(Convolution2D(128, (3,3), activation='relu',padding='same', dilation_rate=(2, 2)))
    model.add(Convolution2D(128, (3,3), activation='relu',padding='same', dilation_rate=(2, 2)))
    
    model.add(SpatialPyramidPooling([1,2]))
    model.add(Dense(21, activation='relu', name="Dense_1"))
    
    model.add(Dense(21, activation='relu', name="Dense_2"))
    
    model.add(Dense(1, activation='linear', name="Dense_3"))
    if(weights_path):
	    model.load_weights(weights_path)

    return model
    
def trainModel(path, nbEpoch,weights_Recognizer):
    
    with open(path+"base_app.p","r") as fp:
        baseApp=pickle.load(fp)
    with open(path+"base_valid.p","r") as fp:
        baseValid = pickle.load(fp)
    with open(path+"base_test.p","r") as fp:
        test = pickle.load(fp)
    model = creerModel()

    freq_save_weight = 10
    filesave = "save_metric.txt"    
    
    model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.0001))
    
    fichier = open('save_metric.txt','w')
    fichier.close()
    
    for epoch in range(1,nbEpoch+1):
        
        lossEpoch = 0
        accEpoch = 0
        IoUEpoch = 0
        n = 0;
        random.shuffle(baseApp)
        for fileApp in baseApp:
            n+=1
            batch= np.expand_dims(fileApp[0], axis=0)
            label = np.array(fileApp[1])

            label = np.expand_dims(label, axis=0)   
            label = np.expand_dims(label, axis=0)

            history = model.train_on_batch(batch,label)
            get_output = K.function([model.layers[0].input], [model.layers[-1].output])
            my_output = get_output([batch])[0]
            print my_output
            lossEpoch += history


            #print("loss = ", history[0], "acc = ", history[1], "IoU = ", history[2])
        lossEpoch = lossEpoch/n

        print(lossEpoch)#, history[2], history[3])
            
        fic = open(filesave,"a+")
        fic.write(str(lossEpoch)+"\t")
        fic.close()
            
        '''
        Partie validation
        '''
        lossEpoch = 0;
        accEpoch = 0;
        IoUEpoch = 0
        n = 0;
        for fileValid in baseValid:
            n=n+1

            batch= np.expand_dims(fileValid[0], axis=0)
            label = np.array(fileValid[1])

            label = np.expand_dims(label, axis=0)
            label = np.expand_dims(label, axis=0)

            history = model.test_on_batch(batch,label)
            lossEpoch += history

            
        lossEpoch = lossEpoch/n

        print(lossEpoch)
        fic = open(filesave,"a+")
        fic.write(str(lossEpoch)+"\n")
        fic.close()
        
        if epoch%freq_save_weight == 0:
            model.save('weights/model_{}_{}.h5'.format(weights_Recognizer,epoch))
        

        
    

if __name__=="__main__":
    path=""
    epoch = 100
    trainModel(path,epoch,"test1")
    
    