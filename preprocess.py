import sys
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
print(tips)
print(Xsections)
