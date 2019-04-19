import numpy as np
import cv2
import sys
import math
import os

from utils import *

rectangles = []

black_sizes = []
angles = []
centroids = []
ratios = []
transitions = []
normalized_sizes = []
normalized_sums = []

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

		if blacks == 0:
			normalized_sizes.append(0)
		else:
			normalized_sizes.append((right-left) * (bottom-top) / blacks)

		if cx == left:
			angle = math.pi / 2
		else:
			angle = math.atan((float)((bottom-cy) / (float)(cx-left)))
		angles.append(angle)

		centroids.append((cx, cy))

		try:	
			ratios.append( (right-left)/(bottom-top) )
		except:
			ratios.append( 0 )

		transitions.append( findTransitions(image, left, right, top, bottom) )

		normalized_sums.append( blackPixelAngleSummation(image, left, right, top, bottom) )


if __name__ == '__main__':

	src = sys.argv[1]
	dst = sys.argv[2]

	if not os.path.isdir( dst ):
		os.mkdir(dst)

	for img_file in os.listdir(src):
		rectangles = []

		black_sizes = []
		angles = []
		centroids = []
		ratios = []
		transitions = []
		normalized_sizes = []
		normalized_sums = []
		
		img_name = img_file.split('.')[0]

		print(img_name)

		out_folder = os.path.join(dst, img_name)
		if not os.path.isdir( out_folder ):
			os.mkdir(out_folder)
		else:
			continue

		img_full = os.path.join(src, img_file)
		img = cv2.imread(img_full, 0)

		img = binarization(img)
		top, bottom, right, left = bounding_box(img)
		print('Spliting...')
		split(img, left, right, top, bottom)

		blacks_out = open(os.path.join(out_folder, 'blacks.txt'), 'w')
		angles_out = open(os.path.join(out_folder, 'angles.txt'), 'w')
		transitions_out = open(os.path.join(out_folder, 'transitions.txt'), 'w')
		centroids_out = open(os.path.join(out_folder, 'centroids.txt'), 'w')
		ratios_out = open(os.path.join(out_folder, 'ratios.txt'), 'w')
		normalized_sizes_out = open(os.path.join(out_folder, 'normalized_sizes.txt'), 'w')
		normalized_sums_out = open(os.path.join(out_folder, 'normalized_sums.txt'), 'w')

		print('Writing to files...')

		# drawing rectangles, and writing to files
		for i in range(len(rectangles)):
			img = cv2.rectangle( img, (rectangles[i][0][0], rectangles[i][0][1]), (rectangles[i][1][0], rectangles[i][1][1]), (0,0,0), 1)

			centroids_out.write(str(centroids[i])+'\n')
			transitions_out.write(str(transitions[i])+'\n')
			ratios_out.write(str(ratios[i])+'\n')
			blacks_out.write(str(black_sizes[i])+'\n')
			angles_out.write(str(angles[i])+'\n')
			normalized_sizes_out.write(str(normalized_sizes[i])+'\n')
			normalized_sums_out.write(str(normalized_sums[i])+'\n')

		# save images with drawn cells
		cv2.imwrite(os.path.join(out_folder,'out.png'), img)
		# closing files
		normalized_sizes_out.close(); blacks_out.close(); normalized_sums_out.close(); blacks_out.close(); angles_out.close(); centroids_out.close(); transitions_out.close(); ratios_out.close()
		print()