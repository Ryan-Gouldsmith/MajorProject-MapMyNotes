import cv2
import sys
import numpy as np
import os

# Ideas from the tutoral http://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html#gsc.tab=0

GRAYSCALE = 0

image = cv2.imread(sys.argv[1], GRAYSCALE)

image_blurred = cv2.medianBlur(image, 5)

kernel = np.ones((5,5),np.uint8)
older = cv2.erode(image_blurred,kernel,iterations = 1)

adaptive_image = cv2.adaptiveThreshold(older, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 2)

filename, file_extension = os.path.splitext(sys.argv[1])

image_path = "images/gaussian_adaptive_threshold_" + filename + ".tiff"

cv2.imwrite(image_path, adaptive_image)
