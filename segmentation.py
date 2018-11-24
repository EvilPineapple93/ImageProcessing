import xml.etree.ElementTree as ET
import sys
import math
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
    return strokeUnity

def angleAlt(stroke):
    alt = 0
    cnt = 0
    for i in range(2, len(stroke)):
        x3  = stroke[i][0]
        y3  = stroke[i][1]
        x2  = stroke[i-1][0]
        y2  = stroke[i-1][1]
        x1  = stroke[i-2][0]
        y1  = stroke[i-2][1]
        dif = abs(math.atan2((y3-y2),(x3-x2)) - math.atan2((y2-y1),(x2-x1)))
        if dif >= 0.15:
            alt = alt + dif
            cnt = cnt + 1
    return cnt

def vertStd(stroke):
    yavg = 0
    for p in stroke:
        yavg = yavg + p[1]
    yavg = yavg/len(stroke)
    ystd = 0
    for p in stroke:
        ystd = ystd + (p[1]-yavg)**2
    return math.sqrt(ystd/len(stroke))

def horzStd(stroke):
    xavg = 0
    for p in stroke:
        xavg = xavg + p[1]
    xavg = xavg/len(stroke)
    xstd = 0
    for p in stroke:
        xstd = xstd + (p[1]-xavg)**2
    return math.sqrt(xstd/len(stroke))

def complexity(stroke, avgL):
    c = angleAlt(stroke)*2
    m = length(stroke)/avgL*0.5
    d = min(horzStd(stroke), vertStd(stroke))
    if d < 0.005:
        c = c*m*d/0.01
    else:
        c = c*m

    if c >= 30:
        #print('c: ', c)
        return 'c'
    elif c >= 5:
        #print('s: ', c)
        return 's'
    else:
        #print('p: ', c)
        return 'p'

def dataExport(strokeList):
	outFile = open("segmentExportData.txt","w+")
	for e in strokeList:
		outFile.write("%s\r\n" % str(e))
	outFile.write("*")
	for i in range(1, len(strokeList)):
		s1 = strokeList[i-1]
		s2 = strokeList[i]
		outFile.write(str(strokeU(s1,s2)))
	outFile.close()
	

# Determine xml prefix to be removed when parsing data
tree = ET.parse(sys.argv[1])
root = tree.getroot()
pre  = (root.tag).rstrip('ink')

# Strip file number from file name
def nstrip(filename):
    num = []
    i = 1
    fname = filename
    c = filename[-i]
    while c.isdigit():
        fname = fname.rstrip(c)
        num.append(c)
        i = i + 1
        c = filename[-i]
    num = num[::-1]
    num = int(''.join(str(d) for d in num))
    suf = str(num).zfill(3)
    return fname + suf


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
for s in strokeList:
    complexity(s, avgL)
#    print('angleAlt: ', angleAlt(s), 'length: ', length(s), 'std: ', min(horzStd(s), vertStd(s)))

for i in range(1, len(strokeList)):
    s1 = strokeList[i-1]
    s2 = strokeList[i]

x = input('Display? (y/n)')
if x == 'y':
	plotME(strokeList)

groups = []
i = 3
j = 0
while j < len(strokeList):
    flag  = True
    f2    = True
    f3    = True
    if len(strokeList)-j >= 4:
        s1    = strokeList[i-3]
        s2    = strokeList[i-2]
        s3    = strokeList[i-1]
        s4    = strokeList[i]
        c1    = complexity(s1, avgL)
        c2    = complexity(s2, avgL)
        c3    = complexity(s3, avgL)
        c4    = complexity(s4,   avgL)
    elif len(strokeList)-j >= 3:
        s1    = strokeList[i-3]
        s2    = strokeList[i-2]
        s3    = strokeList[i-1]
        c1    = complexity(s1, avgL)
        c2    = complexity(s2, avgL)
        c3    = complexity(s3, avgL)
        c4    = 'x'
        f3    = False
    elif len(strokeList)-j >= 2:
        s1    = strokeList[i-3]
        s2    = strokeList[i-2]
        c1    = complexity(s1, avgL)
        c2    = complexity(s2, avgL)
        c3    = 'x'
        f2    = False
    else:
        s1    = strokeList[i-3]
        group = [s1]
        groups.append(group)
        flag = False


    group = [s1]
    if c1 == 'c' and c2 == 'c' and flag:
        groups.append(group)
        flag = False

    s = 1
    #if c1 == 'c':
        #s = 0.95
    #elif c1 == 'p':
        #s = 1.05

    m = 1
    #if c2 == 'c':
        #m = s*0.95
    #elif c2 == 'p':
        #m = s*1.05

    if flag:
        s12 = m*strokeU(s1, s2)
        if s12 >= 0.5:
            group.append(s2)
        else:
            groups.append(group)
            flag = False

        if f2 and ((c1 == 'c' or c2 == 'c') and c3 == 'c') and flag:
            groups.append(group)
            flag = False

        #if c3 == 'c':
         #   m = s*0.95
        #elif c3 == 'p':
          #  m = s*1.05

        if f2 and flag:
            s13 = m*strokeU(s1, s3)
            if s13 >= 0.55:
                group.append(s3)
            else:
                groups.append(group)
                flag = False

            if f3 and ((c1 == 'c' or c2 == 'c' or c3 == 'c') and c4 == 'c') and flag:
                groups.append(group)
                flag = False

            #if c4 == 'c':
            #    m = s*0.95
            #elif c4 == 'p':
             #   m = s*1.05

            if f3 and flag:
                s14 = m*strokeU(s1, s4)
                if s14 >= 0.6:
                    group.append(s4)
                else:
                    groups.append(group)
                    flag = False

                if flag:
                    groups.append(group)

    i = i + len(group)
    j = j + len(group)
equation = sys.argv[1].rstrip('.inkml')
np.save(nstrip(equation),np.asarray(groups))
