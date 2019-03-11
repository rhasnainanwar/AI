import numpy as np
import cv2
import sys

from Task_1 import bounding_box
from Task_2 import findCentroid
from Task_4 import findTransitions

rectangles = []
centroids = []
transitions = []
ratios = []

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

	transitions_out = open(img_name+'_transitions.txt', 'w')
	centroids_out = open(img_name+'_centroids.txt', 'w')
	ratios_out = open(img_name+'_ratios.txt', 'w')

	print('Writing to files...')

	# drawing rectangles, and writing to files
	for i in range(len(rectangles)):
		img = cv2.rectangle( img, (rectangles[i][0][0], rectangles[i][0][1]), (rectangles[i][1][0], rectangles[i][1][1]), (0,0,0), 1)
		transitions_out.write(str(transitions[i])+'\n')
		ratios_out.write(str(ratios[i])+'\n')
		centroids_out.write(str(centroids[i])+'\n')

	# save images with drawn cells
	cv2.imwrite(img_name+'_out.png', img)
	transitions_out.close(); centroids_out.close(); ratios_out.close()