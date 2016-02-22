import cv2
import numpy as np
import copy
import sys
import os

img = cv2.imread(sys.argv[1])
height, width, depth = img.shape

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

#http://stackoverflow.com/questions/17877940/define-black-region-in-hsv-color-space
lower_black = np.array([0,0,0])
upper_black = np.array([175,20, 95])

kernel = np.ones((3,3),np.uint8)



# OpenCV library tutorials
hsv = cv2.erode(hsv,kernel,iterations = 1)

#hsv = cv2.adaptiveThreshold(hsv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 1)

#OpenCV library tutorials
mask_black = cv2.inRange(hsv, lower_black, upper_black)

mask_black = cv2.medianBlur(mask_black,1,0)

# Zeros Adapted from http://stackoverflow.com/questions/16235955/create-a-multichannel-zeros-mat-in-python-with-cv2
mask = np.zeros((height,width),np.uint8)

# Found a better way than itterating over the whole pixels http://stackoverflow.com/questions/30331944/finding-red-color-using-python-opencv
mask[np.where(mask_black == 0)] = 255

kernel = np.ones((1,1),np.uint8)

mask = cv2.dilate(mask,kernel,iterations = 1)

thresh7 = cv2.medianBlur(mask,3,0)

#

#ret3,thresh7 = cv2.threshold(mask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)








#kernel = np.ones((1,1),np.uint8)
#kernel = np.ones((9,9),np.uint8)

#thresh7 = cv2.erode(thresh7,kernel,iterations = 1)

#kernel = np.ones((4,4),np.uint8)
#kernel = np.ones((1,1),np.uint8)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

thresh7 = cv2.morphologyEx(thresh7, cv2.MORPH_OPEN, kernel)

image_path = "test_new_blue.tiff"

cv2.imwrite(image_path, thresh7)

cv2.imshow("im", thresh7)
cv2.waitKey(0)
cv2.destroyAllWindows()
