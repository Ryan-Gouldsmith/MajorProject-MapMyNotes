#!/usr/bin/python

import os
import cv2
import numpy as np


class Blueline_Adaptive_Threshold(object):

    GRAYSCALE_VALUE = 0

    def image_file_exists(self, filename):
        # Going up a directory http://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
        script_root = os.path.dirname(os.path.dirname(__file__))
        return os.path.isfile(os.path.join(script_root, filename))


    def read_image(self, filename):
        if self.image_file_exists(filename):
            self.grayscale_image = cv2.imread(filename)
        else:
            return None

        return self.grayscale_image












if __name__ == "__main__":

    true_or_false = image_file_exists("foo")

# Take an image from the input and convert it to grayscale

# perform smoothing and run threshold

# save the image
