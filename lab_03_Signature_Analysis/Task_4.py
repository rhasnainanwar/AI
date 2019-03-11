"""
We implement black to white transition algorithm for the OTSU binarized image.
"""

def findTransitions(img, left, right, top, bottom):
	height, width = img.shape
	prevPixel = img[0,0]
	countBW = 0
	for x in range(left, right):
		for y in range(top, bottom):
			curPixel = img[y,x]
			if (curPixel == 255) and (prevPixel == 0):
				countBW += 1
			prevPixel = curPixel
	return countBW