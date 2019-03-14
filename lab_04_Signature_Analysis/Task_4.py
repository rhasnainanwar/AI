"""
We implement black to white transition algorithm for the OTSU binarized image.
"""

def findBlacks(img, left, right, top, bottom):
	countBW = 0
	for x in range(left, right):
		for y in range(top, bottom):
			curPixel = img[y,x]
			if (curPixel == 0):
				countBW += 1
	return countBW