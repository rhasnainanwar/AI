import numpy as np
import cv2
import sys
import math

from utils import *

rectangles = []

black_sizes = []
angles = []
centroids = []
ratios = []
transitions = []


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
		blacks = findBlacks(image, left, right, top, bottom)
		
		try:	
			black_sizes.append(size/blacks)
		except:
			black_sizes.append(0)

		if cx == left:
			angle = math.pi / 2
		else:
			angle = math.atan((float)((bottom-cy) / (float)(cx-left)))
		angles.append(angle)

		centroids.append((cx, cy))

		ratios.append( (right-left)/(bottom-top) )

		transitions.append( findTransitions(image, left, right, top, bottom) )

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
	transitions_out = open(img_name+'_transitions.txt', 'w')
	centroids_out = open(img_name+'_centroids.txt', 'w')
	ratios_out = open(img_name+'_ratios.txt', 'w')

	print('Writing to files...')

	# drawing rectangles, and writing to files
	for i in range(len(rectangles)):
		img = cv2.rectangle( img, (rectangles[i][0][0], rectangles[i][0][1]), (rectangles[i][1][0], rectangles[i][1][1]), (0,0,0), 1)

		centroids_out.write(str(centroids[i])+'\n')
		transitions_out.write(str(transitions[i])+'\n')
		ratios_out.write(str(ratios[i])+'\n')
		blacks_out.write(str(black_sizes[i])+'\n')
		angles_out.write(str(angles[i])+'\n')

	# save images with drawn cells
	cv2.imwrite(img_name+'_out.png', img)
	blacks_out.close(); angles_out.close();