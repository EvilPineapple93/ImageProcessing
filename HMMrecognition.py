import sys
import numpy as np
import scipy.spatial as sp 
import matplotlib.pyplot as plt
from hmmlearn import hmm
f = np.array([])
file = open(“segmentExportData.txt”, “r”) 
for e in file:
    print np.append(file.readline())

    


X = np.concatenate([observations, results])
lengths = [len(obserations), len(results)]


model = hmm.GaussianHMM(n_components=50, covariance_type="full", n_iter=100)
model.fit(X)





