import sys
import numpy as np
import scipy.spatial as sp 
import matplotlib.pyplot as plt
from hmmlearn import hmm

strokeList = np.load("strokeList.npy")
unityList = np.load("unityList.npy")



X = np.concatenate([observations, results])
lengths = [len(obserations), len(results)]

model = hmm.GaussianHMM(n_components=50, covariance_type="full", n_iter=100)
model.fit(X)





