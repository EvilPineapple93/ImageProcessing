import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import color
from skimage.morphology import skeletonize

def bw2wb(image):
    im = image - 1
    im = abs(im)
    return im

def neighbours(sl):
    return np.sum(sl) - 1

def findTips(image):
    tips = []
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            if image[i,j] == 1:
                minx = max(i-1, 0)
                maxx = min(i+2, len(image))
                miny = max(j-1, 0)
                maxy = min(j+2, len(image[0]))
                sl = np.int_(image[minx:maxx, miny:maxy])
                n = neighbours(sl)
                if n == 1:
                    tips.append([i,j])
    return tips

def findXSections(image):
    Xsections = []
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            if image[i,j] == 1:
                minx = max(i-1, 0)
                maxx = min(i+2, len(image))
                miny = max(j-1, 0)
                maxy = min(j+2, len(image[0]))
                sl = np.int_(image[minx:maxx, miny:maxy])
                n = neighbours(sl)
                if n >= 3:
                    Xsections.append([i,j])
    return Xsections

def visited(point, stroke):
    for p in stroke:
        if p[0] == point[0] and p[1] == point[1]:
            return True
    return False

def removePoint(point, adj):
    trimmed = []
    for p in adj:
        if p[0] != point[0] or p[1] != point[1]:
            trimmed.append(p)
    return trimmed

def getAdjacent(point, im):
    adj = []
    for i in range(point[0]-1, point[0]+2):
        for j in range(point[1]-1, point[1]+2):
            if im[i,j] > 0:
                adj.append([i,j])
    adj = removePoint(point, adj)
    return adj

def nearests(current, adj):
    near = []
    min = 2
    for p in adj:
        x = abs(current[0] - p[0])
        y = abs(current[1] - p[1])
        d = x+y
        if d < min:
            min = d
    for p in adj:
        x = abs(current[0] - p[0])
        y = abs(current[1] - p[1])
        d = x+y
        if d == min:
            near.append(p)
    return near

def smoothest(current, prev, adj):
    pslope = math.atan2(current[0]-prev[0], current[1]-prev[1])
    slopes = []
    for p in adj:
        slopes.append(math.atan2(p[0]-current[0], p[1]-current[1]))
    minsl = abs(pslope - slopes[0])
    index = 0
    for i in range(1, len(slopes)):
        dif = abs(pslope - slopes[i])
        if dif < minsl:
            minsl = dif
            index = i
    return adj[i]

def nextPoint(current, stroke, im):
    adj = getAdjacent(current, im)
    for p in adj:
        if visited(p, stroke):
            adj = removePoint(p, adj)
    if len(adj) == 0:
        return current
    elif len(adj) == 1:
        return adj[0]
    else:
        near = nearests(current, adj)
        if len(near) == 1:
            return near[0]
        else:
            return smoothest(current, stroke[-2], adj)

def vectorize(tip, im):
    stroke = []
    stroke.append(tip)
    current = tip
    next = nextPoint(current, stroke, im)
    while next[0] != current[0] or next[1] != current[1]:
        stroke.append(next)
        current = next
        next = nextPoint(current, stroke, im)
    last = getAdjacent(current, im)
    last = removePoint(stroke[-1], last)
    if len(last) == 1:
        stroke.append(last[0])
    else:
        n = nearests(current, last)
        if len(n) == 1:
            stroke.append(n[0])
        else:
            stroke.append(smoothest(current, stroke[-2], last))
    return rcols2xy(stroke)

def rcols2xy(vstroke):
    stroke = []
    for p in vstroke:
        p2 = [p[1], p[0]]
        stroke.append(p2)
    return np.asarray(stroke)

filename = sys.argv[1]
print(filename)
image    = io.imread(filename)
image    = color.rgb2grey(image)
image    = bw2wb(image)
#io.imshow(image)
#io.show()
skeleton = skeletonize(image)
io.imshow(skeleton)
io.show()
tips = findTips(skeleton)
tips = np.asarray(tips)
Xsections = findXSections(skeleton)
Xsections = np.asarray(Xsections)
stroke = vectorize(tips[0], skeleton)
stroke = stroke/1000
for i in range(1, len(stroke) - 1):
    stroke[i][0] = (stroke[i-1][0]+stroke[i+1][0])/2
    stroke[i][1] = (stroke[i-1][1]+stroke[i+1][1])/2

for i in range(2, len(stroke) - 2):
    stroke[i][0] = (stroke[i-2][0]+stroke[i+2][0])/2
    stroke[i][1] = (stroke[i-2][1]+stroke[i+2][1])/2
print(stroke)
plt.plot(stroke[:,0], -stroke[:,1])
#plt.plot(stroke[:,1], -stroke[:,0])
plt.axes().set_aspect('equal')
plt.show()
