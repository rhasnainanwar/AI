from PIL import Image
from PIL import ImageDraw
import cv2
from math import atan
import numpy as np

tran = {}
aspect = {}
blackPixelList = {}
centroidList = {}
normalizedSize = {}
angleList = {}
summationAngleList = {}


def binarize(img, thre, width, height):
	for x in range(0, width):
		for y in range(0, height):
			r, g, b = img.getpixel((x, y))
			avg = (r + g + b) / 3        # get the pixel and average all of them
			if avg > thre:        # if > threshold, set to  1 else set to 0
				avg = 255
			else:
				avg = 0
			img.putpixel((x, y), (avg, avg, avg))
	
	return img


# Finding the Centroid
# Based on Given Co-ordinates
def centroid(img, x1, y1, x2, y2):
	cx = 0
	cy = 0
	n = 0
	for y in range(y1, y2):
		for x in range(x1, x2):
			r, g, b = img.getpixel((x, y))
			avg = (r + g + b) / 3       # For black pixel. update the current storage
			if avg == 0:
				cx += x
				cy += y
				n += 1
	
	if n == 0:
		return ((x1 + x2) / 2, (y1 + y2) / 2, n)
	else:
		return (cx / n, cy / n, n)        # return the avg values


# Black to White Transitions
def blackToWhiteTransition(img, x1, y1, x2, y2):

	count = 0
	width,height=img.size
	for y in range(y1, y2):
		for x in range(x1, x2):
			r, g, b = img.getpixel((x, y))    # Current Pixel is Black and Next is white, add up
			avg = (r + g + b) / 3
			if(x + 1 == width):
				continue
			r1, g1, b1 = img.getpixel((x + 1, y))
			
			avg1 = (r1 + g1 + b1) / 3
			
			if avg == 0 and avg1 == 255:
				count += 1
	
	
	return count


def blackPixelAngleSummation(img, x1, y1, x2, y2):
	sum = 0
	blackCount = 0
	
	for x in range(x1, x2):
		for y in range(y1, y2):
			r, g, b = img.getpixel((x, y))
			avg = (r + g + b) / 3
			if(avg == 0):
				blackCount += 1
				if(x == x1):
					sum += math.pi / 2
				else:
					sum += atan ((float) (y2-y)  / (float) (x-x1))
	
	
	if(blackCount == 0):
		return 0
	return sum / blackCount
				

def boundingBox(img, x_1, y_1, x_2, y_2):
	x1, y1 = x_2, y_2
	x4, y4 = x_1, y_1
	for y in range(y_1, y_2):
		for x in range(x_1, x_2):
			r, g, b = img.getpixel((x, y)) 
			
			if y + 1 < height:
				r1, g1, b1 = img.getpixel((x, y + 1))
			else:
				r1, g1, b1 = 255, 255, 255
				
			if x + 1 < width:
				r2, g2, b2 = img.getpixel((x + 1, y))
			else:
				r2, g2, b2 = 255, 255, 255
			
			avg = (r + g + b) / 3
			# y+1 Pt
			avg1 = (r1 + g1 + b1) / 3
			# X+1 Pt
			avg2 = (r2 + g2 + b2) / 3    

			# Get the Minimum Point
			# Here we get the black pixel with is at least distance from the start
			if avg == 0  and x < x1:
				x1 = x
			if avg == 0  and y < y1:
				y1 = y
			if avg == 0  and x > x4:
				x4 = x
			if avg == 0  and y > y4:
				y4 = y
					
	
	draw = ImageDraw.Draw(img)
	draw.rectangle(((x1, y1), (x4, y4)), fill=None, outline="red")
#    img2=img.crop((x1,y1,x4,y4))
#    img2.save("borderImage.png")
	return img


def spliceImage(img, x1, y1, x2, y2, recVal, spliceVal=""):
	cx, cy, blackPixels = centroid(img, x1, y1, x2, y2)
	if recVal < 3:
		
		spliceImage(img, x1, y1, cx, cy, recVal + 1, spliceVal + "A")
		spliceImage(img, cx, y1, x2, cy, recVal + 1, spliceVal + "B")
		spliceImage(img, x1, cy, cx, y2, recVal + 1, spliceVal + "C")
		spliceImage(img, cx, cy, x2, y2, recVal + 1, spliceVal + "D")
	
	elif recVal == 3:
		transitions = blackToWhiteTransition(img, x1, y1, x2, y2)
		aspect_ratio = (x2-x1) / (y2-y1)
		draw = ImageDraw.Draw(img)
		draw.rectangle(((x1, y1), (x2, y2)), fill=None, outline="red")
		
		tran[spliceVal] = transitions
		aspect[spliceVal] = aspect_ratio
		centroidList[spliceVal] = cx, cy
		#Storing the Black Pixels
		blackPixelList[spliceVal] = blackPixels
		# Storing the Angle
		
		if cx == x1:
			angleList[spliceVal] = math.pi / 2
		else:
			angleList[spliceVal] = atan((float)((y2-cy) / (float)(cx-x1)))
		
		summationAngleList[spliceVal] = blackPixelAngleSummation(img, x1, y1, x2, y2)
		
		if blackPixels == 0:
			normalizedSize[spliceVal] = 0
		else:
			normalizedSize[spliceVal] = ((x2-x1) * (y2-y1) / blackPixels)