import sys
import numpy as np
import scipy.spatial as sp 
import matplotlib.pyplot as plt
from hmmlearn import hmm

    










X = np.concatenate([observations, results])
lengths = [len(obserations), len(results)]


model = hmm.GaussianHMM(n_components=50, covariance_type="full", n_iter=100)
model.fit(X)





strokeList = np.load("strokeList.npy")
print(strokeList)

strokeList = np.load("unityList.npy")
print(strokeList)