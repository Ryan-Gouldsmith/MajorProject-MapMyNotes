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
