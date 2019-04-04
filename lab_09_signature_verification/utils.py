"""
We implement bounding box algorithm for the OTSU binarized image.
"""

def bounding_box(img):
	height, width = img.shape
	left, right = width, 0
	top, bottom = height, 0

	for x in range(width):
		for y in range(height):
			color = img[y,x]
			if color == 0:
				if x > right:
					right = x
				if x < left:
					left = x 
				if y > bottom:
					bottom = y
				if y < top:
					top = y

	print("The bounding box is:")
	print("Top: ", top, " Bottom: ", bottom, " Left: ", left, " Right: ", right)
	return top, bottom, right, left


"""
We implement centroid computing algorithm for the OTSU binarized image.
"""
def findCentroid(img, left, right, top, bottom):
	cx, cy, n = 0, 0, 0
	for x in range(left, right):
		for y in range(top, bottom):
			if img[y,x] == 0:
				cx = cx + x 
				cy = cy + y
				n += 1
	if n == 0:
		return cx, cy		
	cx = cx // n
	cy = cy // n

	return cx, cy


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