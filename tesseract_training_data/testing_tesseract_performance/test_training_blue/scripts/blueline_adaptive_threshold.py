#!/usr/bin/python

import os
import cv2
import numpy as np
import sys


class Blueline_Adaptive_Threshold(object):

    # Based upon and adaptive from methods found on the open cv tutorial page http://docs.opencv.org/3.1.0/d7/d4d/tutorial_py_thresholding.html about adaptive thresholding.

    GRAYSCALE_VALUE = 0
    SMALL_KERNEL_SIZE = 2
    ERODE_ITERATION = 1

    LOWER_BLACK_HUE = 0
    LOWER_BLACK_SATURATION = 0
    LOWER_BLACK_VALUE = 0

    UPPER_BLACK_HUE = 175
    UPPER_BLACK_SATURATION = 20
    UPPER_BLACK_VALUE = 95

    BLACK_VALUE = 255
    WHITE_VALUE = 0

    ADAPTIVE_THRESHOLD_BLOCK_SIZE = 13
    ADAPTIVE_THRESHOLD_WEIGHTED_MEAN = 2

    IMAGE_EXTENSION = ".tiff"


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
        # Used to learn how to smooth an image http://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html#gsc.tab=0
        return np.ones((kernel_size,kernel_size),np.uint8)

    def erode_image(self, greyscale_image, kernel_size):
        eroded_image = cv2.erode(greyscale_image,kernel_size,iterations = self.ERODE_ITERATION)

        return eroded_image

    def black_text_extraction(self, erroded_image):
        #http://stackoverflow.com/questions/17877940/define-black-region-in-hsv-color-space
        lower_black_scale = np.array([self.LOWER_BLACK_HUE, self.LOWER_BLACK_SATURATION, self.LOWER_BLACK_VALUE])

        upper_black_scale = np.array([self.UPPER_BLACK_HUE, self.UPPER_BLACK_SATURATION, self. UPPER_BLACK_VALUE])

        self.black_text = cv2.inRange(erroded_image, lower_black_scale, upper_black_scale)

        return self.black_text

    def get_image_dimensions(self):
        return self.image.shape

    def get_blank_image_mask(self):
        height, width, depth = self.get_image_dimensions()
        # Zeros Adapted from http://stackoverflow.com/questions/16235955/create-a-multichannel-zeros-mat-in-python-with-cv2
        self.blank_mask = np.zeros((height,width),np.uint8)

        return self.blank_mask

    def convert_text_extraction_to_mask(self):
        self.blank_mask[np.where(self.black_text == self.WHITE_VALUE)] = self.BLACK_VALUE

        return self.blank_mask

    def apply_threshold(self, mask):
        self.threshold_image = cv2.adaptiveThreshold(mask, self.BLACK_VALUE, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.ADAPTIVE_THRESHOLD_BLOCK_SIZE, self.ADAPTIVE_THRESHOLD_WEIGHTED_MEAN)

        return self.threshold_image

    def save_adaptive_threshold_image(self, filename):
        filename, file_extension = os.path.splitext(filename)
        print filename

        image_path = filename + self.IMAGE_EXTENSION

        cv2.imwrite(image_path, self.threshold_image)












if __name__ == "__main__":


    threshold = Blueline_Adaptive_Threshold()
    # Read in an image as colour
    image = threshold.read_image(sys.argv[1])

    # Take an image from the input and convert it to grayscale
    grayscale_image = threshold.convert_to_grayscale(image)

    # Clear up the image by eroding.
    kernel = threshold.get_kernel(2)

    eroded_image = threshold.erode_image(grayscale_image, kernel)

    black_text = threshold.black_text_extraction(eroded_image)

    mask = threshold.get_blank_image_mask()

    mask = threshold.convert_text_extraction_to_mask()

    kernel = threshold.get_kernel(5)

    eroded_mask = threshold.erode_image(mask, kernel)

    threshold.apply_threshold(eroded_mask)

    threshold.save_adaptive_threshold_image(sys.argv[1])

    








# perform smoothing and run threshold

# save the image
