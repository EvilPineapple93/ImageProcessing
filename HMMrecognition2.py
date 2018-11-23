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

strokeList = np.load("strokeList.npy")
unityList = np.load("unityList.npy")
for i in range(0, len(strokeList)):
    strokeList[i][:,0] = strokeList[i][:,0] - np.min(strokeList[i][:,0])
    strokeList[i][:,1] = strokeList[i][:,1] - np.min(strokeList[i][:,1])

Zeros = np.empty((32,32))
dir_path = os.path.dirname(os.path.realpath('../Zeros/train_30_30047.png'))
n =1
for filename in os.listdir('../Zeros/'):
    filename = dir_path + str("/"+filename)
    image = mpimg.imread(filename)
    #img = tf.image.decode_png(tf.read_file(filename))
    image = Image.open(filename).convert('L')
    basewidth = 32
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth,hsize), Image.ANTIALIAS)
    image = np.array(image)
    #image = image.reshape(-1)
    Zeros = np.concatenate((Zeros,image), axis=0)
    n = n+1


Zeros = Zeros.reshape(basewidth**2,n)
ZeroM = hmm.GaussianHMM(n_components=2, covariance_type="diag", init_params="cm", params="cmt")
ZeroM.startprob_ = np.array([1.0, 0.0])
ZeroM.transmat_ = np.array([ [0.8, 0.2], [0.0, 1.0] ])
Zeros = Zeros.T
for test in Zeros:
    test = test.reshape(-1,1)
    print test
    ZeroM.fit(test)

Ones = np.empty((32,32))
dir_path = os.path.dirname(os.path.realpath('../Ones/train_31_10438.png'))
n = 0
for filename in os.listdir('../Ones/'):
    filename = dir_path + str("/"+filename)
    image = mpimg.imread(filename)
    #img = tf.image.decode_png(tf.read_file(filename))
    
    image = Image.open(filename).convert('L')
    basewidth = 32
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    image = image.resize((basewidth,hsize), Image.ANTIALIAS)
    image = np.array(image)
    #image = image.reshape(-1)
    Ones = np.concatenate((Ones,image), axis=0)
    n = n+1


Ones = Ones.reshape(basewidth**2,n)
OneM = hmm.GaussianHMM(n_components=6, covariance_type="diag", init_params="cm", params="cmt")
OneM.startprob_ = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
OneM.transmat_ = np.array([[0.5, 0.5, 0.0, 0.0, 0.0, 0.0], [0.0, 0.5, 0.5, 0.0, 0.0, 0.0], [0.0, 0.0, 0.5, 0.5, 0.0, 0.0], \
[0.0, 0.0, 0.0, 0.5, 0.5, 0.0], [0.0, 0.0, 0.0, 0.0, 0.5, 0.5], [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
Ones = Ones.T
for test in Ones:
    OneM.fit(test)

joblib.dump(ZeroM, "ZeroMarkov.pkl")
joblib.dump(OneM, "OneMarkov.pkl")





#lr = hmm.GaussianHMM(n_components=3, covariance_type="diag", init_params="cm", params="cmt")
#lr.startprob_ = np.array([1.0, 0.0, 0.0])
#lr.transmat_ = np.array([[0.7, 0.3, 0.0],[0.0, 0.7, 0.3], [0.0, 0.0, 1.0]])
#lr.emissionprob_ = np.array([
#  [1.0, 0.0, 0.0],
#  [0.0, 1.0, 0.0],
#  [0.0, 0.0, 1.0]
#])
#lr.fit(Testing.T)
#test = lr.predict(Testing.T)
#print test


