import numpy as np

import cv2

class TestImage(object):

    def perform_greyscale(self, filename):
        file = "static/" + filename
        # Reference: https://extr3metech.wordpress.com/2012/09/23/convert-photo-to-grayscale-with-python-opencv/
        image = cv2.imread(file)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('static/gray_test.png',gray_image)
        return "gray_test.png"

    def binarise_image(self, filename):
        file = "static/" + filename

        img = cv2.imread(file,0)
        older = cv2.medianBlur(img, 5)

        #smooth, help from http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

        kernel = np.ones((5,5),np.uint8)
        older = cv2.erode(older,kernel,iterations = 1)

        # Adaptive Threshold idea from http://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html#gsc.tab=0
        thresh7 = cv2.adaptiveThreshold(older, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 2)

        cv2.imwrite("static/binary_image.jpg", thresh7)
        return "binary_image.jpg"
