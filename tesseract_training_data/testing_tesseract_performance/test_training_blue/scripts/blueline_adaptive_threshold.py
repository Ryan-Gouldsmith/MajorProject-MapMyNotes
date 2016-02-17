#!/usr/bin/python

import os
import cv2
import numpy as np
import sys


class Blueline_Adaptive_Threshold(object):

    GRAYSCALE_VALUE = 0
    SMALL_KERNEL_SIZE = 2
    ERODE_ITERATION = 1

    def image_file_exists(self, filename):
        # Going up a directory http://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
        script_root = os.path.dirname(os.path.dirname(__file__))
        return os.path.isfile(os.path.join(script_root, filename))

    def read_image(self, filename):
        if self.image_file_exists(filename):
            self.image = cv2.imread(filename)
        else:
            return None

        return self.image

    def convert_to_grayscale(self, image):
        self.grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return self.grayscale_image

    def get_kernel(self, kernel_size):
        return np.ones((kernel_size,kernel_size),np.uint8)

    def erode_image(self, greyscale_image, kernel_size):
        eroded_image = cv2.erode(greyscale_image,kernel_size,iterations = self.ERODE_ITERATION)
        return eroded_image








if __name__ == "__main__":

    # Read in an image as colour
    image = read_image(sys.argv[1])

    # Take an image from the input and convert it to grayscale
    grayscale_image = convert_to_grayscale(image)

    # Clear up the image by eroding.






# perform smoothing and run threshold

# save the image
