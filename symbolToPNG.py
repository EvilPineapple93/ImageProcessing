import sys
import os
import numpy as np
import cv2

# Collect symbol list from .npy file
symbolList = np.load(sys.argv[1])

# Create folder if not already created 
root = sys.argv[1].rstrip('.npy')
if not os.path.exists(root):
    os.makedirs(root)

for i in range(len(symbolList)):
	
	# Scale and center stroke
	symbol = [1000*stroke for stroke in symbolList[i]]
	
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
		img = cv2.polylines(img, [pts], False,(0,0,0),4) 
	
	# Write to png file, will overwrite if file exists
	cv2.imwrite(root+'\symbol_%03d.png' % i,img)
