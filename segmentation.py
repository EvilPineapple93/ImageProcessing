import xml.etree.ElementTree as ET
import sys
import numpy as np
import matplotlib.pyplot as plt

def findXtrema(strokeList):
    xmin = min(np.amin(stroke[:,0]) for stroke in strokeList)
    xmax = max(np.amax(stroke[:,0]) for stroke in strokeList)
    ymin = min(np.amin(stroke[:,1]) for stroke in strokeList)
    ymax = max(np.amax(stroke[:,1]) for stroke in strokeList)
    return [xmin, xmax],[-ymax,-ymin]

def plotME(strokeList):
    for stroke in strokeList:
        plt.plot(stroke[:,0],-stroke[:,1], 'k')
    xlims,ylims = findXtrema(strokeList)
    plt.axes().set_aspect('equal')
    plt.show()
#test

tree = ET.parse(sys.argv[1])
root = tree.getroot()
pre  = (root.tag).rstrip('ink')

strokeList = []
for stroke in root.findall(pre+'trace'):
    coords = stroke.text.split(', ');
    npCoords = []
    for element in coords:
        x,y = element.split(' ')
        npCoords.append([float(x), float(y)])

    npCoords = np.asarray(npCoords)
    strokeList.append(npCoords)

#print(strokeList)
plotME(strokeList)



#fuck

