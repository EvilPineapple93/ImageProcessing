import xml.etree.ElementTree as ET
import sys
import numpy as np
import scipy.spatial as sp 
import matplotlib.pyplot as plt

# Plots mathematical expression, given list of strokes 
def plotME(strokeList):
    for stroke in strokeList:
        plt.plot(stroke[:,0],-stroke[:,1], 'k')
    plt.axes().set_aspect('equal')
    plt.show()

# Calculates minimum distance between two given strokes
def minDist(stroke1, stroke2):
	dmin = sp.distance.pdist([stroke1[0],stroke2[0]], 'euclidean')
	for p1 in stroke1:
		for p2 in stroke2:
			tmp = sp.distance.pdist([stroke1[0],stroke2[0]], 'euclidean')
			if tmp < dmin:
				dmin = tmp
	return dmin


# Determine xml prefix to be removed when parsing data
tree = ET.parse(sys.argv[1])
root = tree.getroot()
pre  = (root.tag).rstrip('ink')

# Parse xml data into a list of strokes
strokeList = []
for stroke in root.findall(pre+'trace'):
    coords = stroke.text.split(', ');
    npCoords = []
	# Convert pair of float strings into tuplet of floats
    for element in coords:
        x,y = element.split(' ')
        npCoords.append([float(x), float(y)])
	# Convert coordinate list into Nx2 numpy matrix
    npCoords = np.asarray(npCoords)
    strokeList.append(npCoords)

plotME(strokeList)
