import xml.etree.ElementTree as ET
import sys
import numpy as np
import scipy.spatial as sp 
import matplotlib.pyplot as plt

# Plots mathematical expression, given list of strokes 
def plotME(strokeList):
    c = 'k'
    plt.plot(strokeList[0][:,0], -strokeList[0][:,1], c)
    for i in range(1, len(strokeList)):
        s1 = strokeList[i-1]
        s2 = strokeList[i]
        if strokeU(s1,s2) < 0.5:
            if c == 'k':
                c = 'b'
            else:
                c = 'k'
        plt.plot(s2[:,0],-s2[:,1], c)
    plt.axes().set_aspect('equal')
    plt.show()

# Calculates minimum distance between two given strokes
def minDist(stroke1, stroke2):
	dmin = sp.distance.pdist([stroke1[0],stroke2[0]], 'euclidean')
	for p1 in stroke1:
		for p2 in stroke2:
			tmp = sp.distance.pdist([p1, p2], 'euclidean')
			if tmp < dmin:
				dmin = tmp
	return dmin

# Determine the horizontal and vertical overlap of the rectangles of the
# strokes
def overlap(stroke1, stroke2):
    xmin1 = min(stroke1[:,0])
    xmax1 = max(stroke1[:,0])
    ymin1 = min(stroke1[:,1])
    ymax1 = max(stroke1[:,1])
    xmin2 = min(stroke2[:,0])
    xmax2 = max(stroke2[:,0])
    ymin2 = min(stroke2[:,1])
    ymax2 = max(stroke2[:,1])
    area1 = (xmax1 - xmin1)*(ymax1 - ymin1)
    area2 = (xmax2 - xmin2)*(ymax2 - ymin2)
    x1    = max(xmin1, xmin2)
    x2    = min(xmax1, xmax2)
    y1    = max(ymin1, ymin2)
    y2    = min(ymax1, ymax2)
    if (x1 > x2 or y1 > y2):
        return 0
    else:
        return (x2 - x1)*(y2 - y1)/min(area1, area2)
    return 0
    
# Distance between starting points of strokes
def startDist(stroke1, stroke2):
    return sp.distance.pdist([stroke1[0], stroke2[0]], 'euclidean')

# Backward movement between the ending point of stroke1 and the starting point
# of stroke2
def endDist(stroke1, stroke2):
    if stroke1[-1][0] > stroke2[0][0]:
        return sp.distance.pdist([stroke1[-1], stroke2[0]], 'euclidean')
    else:
        return 0

# Length of a stroke
def length(s):
    l = 0
    for i in range(1, len(s)):
        l = l + sp.distance.pdist([s[i-1], s[i]], 'euclidean')
    return l

# Average length of a stroke
def avgSLength(strokeList):
    l = 0
    for s in strokeList:
        l = l + length(s)
    return l/len(strokeList)

# Stroke Unity percentage between s1 and s2
def strokeU(s1, s2):
    md = minDist(s1, s2)
    ov = overlap(s1, s2)
    sd = startDist(s1, s2)
    ed = endDist(s1, s2)
    mdP = max(1-md/avgL, 0)
    sdP = max(1-sd/avgL, 0)
    edP = min(ed/avgL, 1.0)
    a = 4
    b = 3
    c = 2
    d = 1
    if (mdP < sdP and mdP < edP and mdp < ov):
        a = 0
    elif (ov < mdP and ov < sdP and ov < edP):
        b = 0
    elif (sdP < mdP and sdP < ov and sdP < edP):
        d = 0
    elif (edP < mdP and edP < ov and edP < sdP):
        c = 0
    if edP == 0:
        c = 0
    strokeUnity = (a*mdP + b*ov + c*edP + d*sdP)/(a+b+c+d)
    print(strokeUnity)
    return strokeUnity

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

avgL = avgSLength(strokeList)
print(avgL)
for i in range(1, len(strokeList)):
    s1 = strokeList[i-1]
    s2 = strokeList[i]
input('Display? (y/n)')

plotME(strokeList)
