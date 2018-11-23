import random                                                                                                                                                                                                  
import tensorflow as tf
import os
import sys
import numpy as np
import scipy.spatial as sp 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from hmmlearn import hmm
from PIL import Image
from sklearn.externals import joblib

ZeroM = joblib.load("ZeroMarkov.pkl") 
OneM =  joblib.load("OneMarkov.pkl") 

Testing = np.empty((1,32**2))
dir_path = os.path.dirname(os.path.realpath('Testing/train_30_30148.png'))
n =0
for filename in os.listdir('Testing/'):
    filename = dir_path + str("/"+filename)                                                                                                                                                                    
    image = mpimg.imread(filename)
    #img = tf.image.decode_png(tf.read_file(filename))     
    image = Image.open(filename).convert('L')
    basewidth = 32
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth,hsize), Image.ANTIALIAS)
    image = np.array(image).reshape((1,32**2))
    #image = image.reshape(-1)
    Testing = np.vstack((Testing,image))
    n= n+1

#Testing = Testing.reshape(basewidth**2,n)  
Testing = np.delete(Testing,0,0)
print Testing.shape
print ZeroM.score(Testing[2].reshape(1,-1))
print OneM.score(Testing[2].reshape(1,-1))

