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