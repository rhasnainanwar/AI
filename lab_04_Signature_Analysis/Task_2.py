
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