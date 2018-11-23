import sys
import numpy as np
import cv2

strokeList = np.load("strokeList.npy")

symbol = [strokeList[1],strokeList[2]]

# Scale and center stroke
symbol = [1000*stroke for stroke in symbol]

xmin = min([min(stroke[:,0]) for stroke in symbol])
xmax = max([max(stroke[:,0]) for stroke in symbol])
ymin = min([min(stroke[:,1]) for stroke in symbol])
ymax = max([max(stroke[:,1]) for stroke in symbol])
xavg = (xmin+xmax)/2
yavg = (ymin+ymax)/2

symbol = [stroke+[64-xavg,64-yavg] for stroke in symbol]

# Initialize canvas
img = np.full((128,128), 255, np.uint8)

# Draw stroke to canvas
for stroke in symbol:
	pts = stroke.astype(np.int32)
	pts = pts.reshape((-1,1,2))
	img = cv2.polylines(img, [pts], False,(0,0,0),5) 

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()