#!/usr/bin/env python
import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt

img = cv2.imread(sys.argv[1],0)
older = cv2.medianBlur(img, 5)

kernel = np.ones((5,5),np.uint8)
older = cv2.erode(older,kernel,iterations = 1)


ret,thresh1 = cv2.threshold(older,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(older,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(older,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(older,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(older,127,255,cv2.THRESH_TOZERO_INV)

thresh6 = cv2.adaptiveThreshold(older,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

# SEEMS LIKE THE GOOD ONE
thresh7 = cv2.adaptiveThreshold(older, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 2)

ret2, thresh8 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#blur = cv2.GaussianBlur(img, (3,3), 0)
ret3, thresh9 = cv2.threshold(older, 127,255,cv2.ADAPTIVE_THRESH_MEAN_C+ cv2.THRESH_BINARY+cv2.THRESH_OTSU)



titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV', "adaptive mean", "Adaptive gaussian", "Otsu", "Otsu + Gaussian"]
images = [older, thresh1, thresh2, thresh3, thresh4, thresh5, thresh6, thresh7, thresh8, thresh9]

for i in xrange(10):
  plt.subplot(2,5,i+1),plt.imshow(images[i],'gray')
  plt.title(titles[i])
  plt.xticks([]),plt.yticks([])

plt.show()

cv2.imshow("image", thresh7)

cv2.waitKey(0)
cv2.destroyAllWindows()
