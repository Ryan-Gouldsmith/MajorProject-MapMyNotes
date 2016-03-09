import cv2
import numpy as np
import copy
import sys
import os

# REFERENCE Ideas considered from, but changed it to match the lines of my own text  http://stackoverflow.com/questions/10196198/how-to-remove-convexity-defects-in-a-sudoku-square

# Excellent resource for extracting lines from music notes. Have been using as a template and how to consider my own line extraction. http://docs.opencv.org/trunk/d1/dee/tutorial_moprh_lines_detection.html#gsc.tab=0
img = cv2.imread(sys.argv[1],0)

#ret3,thresh7 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

img = cv2.medianBlur(img, 7)
thresh7 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 15, 2)
#kernel = np.ones((3,3),np.uint8)
#thresh7 = cv2.erode(thresh7,kernel,iterations = 1)




lines = thresh7.copy()
words = thresh7.copy()

rows, cols = lines.shape

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (75,1))


lines = cv2.erode(lines,kernel,iterations = 1)
lines = cv2.dilate(lines,kernel,iterations = 1)
# SURELY THAT'S JUST DILATING AGAIN?
close = cv2.morphologyEx(lines,cv2.MORPH_DILATE,kernel)


thresh7[np.where(close == 255)] = 0

mask = np.zeros((rows,cols),np.uint8)
mask[np.where(thresh7 == 0)] = 255

kernel = np.ones((3,3),np.uint8)
mask = cv2.dilate(mask,kernel,iterations = 1)


# Reference, updated OpenCV meant that there ws an issue unpacking the variables. http://stackoverflow.com/questions/25504964/opencv-python-valueerror-too-many-values-to-unpack
# here with the tests and script
_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(mask,contours,-1,(255,0,0),thickness=cv2.FILLED)

kernel = np.ones((7,7),np.uint8)
mask = cv2.erode(mask,kernel,iterations = 1)




cv2.imshow("im", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()


filename, file_extension = os.path.splitext(sys.argv[1])

image_path = filename + ".tiff"

#cv2.imwrite(image_path, mask)



"""
kernel = np.ones((3,3),np.uint8)
thresh7 = cv2.erode(thresh7,kernel,iterations = 1)

thresh7 = cv2.medianBlur(thresh7,1,0)













#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#lower_blue = np.array([110,50,50])
#upper_blue = np.array([130,255,255])

#http://stackoverflow.com/questions/17877940/define-black-region-in-hsv-color-space
#lower_black = np.array([0,0,0])
#upper_black = np.array([175,20, 95])

kernel = np.ones((3,3),np.uint8)



# OpenCV library tutorials
hsv = cv2.erode(hsv,kernel,iterations = 1)


#OpenCV library tutorials
mask_black = cv2.inRange(hsv, lower_black, upper_black)



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


thresh7 = cv2.morphologyEx(thresh7, cv2.MORPH_OPEN, kernel)



"""
