import numpy as np
import cv2
import sys
import math

from Task_1 import bounding_box
from Task_2 import findCentroid
from Task_4 import findBlacks

black_sizes = []
rectangles = []
angles = []

def binarization(img):
	retval, binarized_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
	return binarized_img

def split(image, left, right, top, bottom, depth=0):
	# only get smallest cells at lowest level of recursion tree
	cx, cy = findCentroid(image, left, right, top, bottom)
	if depth < 3:
		split(image, left, cx, top, cy, depth + 1)
		split(image, cx, right, top, cy, depth + 1)
		split(image, left, cx, cy, bottom, depth + 1)
		split(image, cx, right, cy, bottom, depth + 1)
	else:
		rectangles.append([(left, top), (right, bottom)])
		# Step 6:  Find the size of each of the 64 cells,
		#		   and normalize them with the number of the black pixels in the cells
		size = (bottom-top)*(right-left)
		print('Size:', size)
		blacks = findBlacks(image, left, right, top, bottom)
		print('Blacks:', blacks)
		
		try:	
			black_sizes.append(size/blacks)
		except:
			black_sizes.append(0)

		# Step 7: Calculate the angle of inclination of each sub-image centre in each cell to lower right corner of the cell. 
		cx, cy = findCentroid(image[top:bottom, left:right], 0, right-left, 0, bottom-top)

		dis = math.sqrt((right-left - cx)**2 + (bottom-top - cy)**2)
		angle = math.acos((bottom-top - cy)/dis)
		angle = math.degrees(angle)
		
		print('Angle:',angle)
		angles.append(angle)

if __name__ == '__main__':
	img_file = sys.argv[1]
	img_name = img_file.split('/')[-1].split('.')[0]
	img = cv2.imread(img_file, 0)

	img = binarization(img)
	top, bottom, right, left = bounding_box(img)
	print('Spliting...')
	split(img, left, right, top, bottom)

	blacks_out = open(img_name+'_blacks.txt', 'w')
	angles_out = open(img_name+'_angles.txt', 'w')

	print('Writing to files...')

	# drawing rectangles, and writing to files
	for i in range(len(rectangles)):
		img = cv2.rectangle( img, (rectangles[i][0][0], rectangles[i][0][1]), (rectangles[i][1][0], rectangles[i][1][1]), (0,0,0), 1)
		blacks_out.write(str(black_sizes[i])+'\n')
		angles_out.write(str(angles[i])+'\n')

	# save images with drawn cells
	cv2.imwrite(img_name+'_out.png', img)
	blacks_out.close(); angles_out.close();