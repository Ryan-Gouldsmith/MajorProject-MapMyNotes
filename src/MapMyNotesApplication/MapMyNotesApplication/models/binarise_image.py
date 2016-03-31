import cv2
import numpy as np
import copy
import sys
import os

"""
REFERENCE Ideas considered from, but changed it to match the lines of my own text  http://stackoverflow.com/questions/10196198/how-to-remove-convexity-defects-in-a-sudoku-square

Excellent resource for extracting lines from music notes. Have been using as a template and how to consider my own line extraction. http://docs.opencv.org/trunk/d1/dee/tutorial_moprh_lines_detection.html#gsc.tab=0
"""
class BinariseImage(object):

    GRAYSCALE_INPUT = 0
    MEDIAN_BLUR_KERNAL_SIZE = 7
    KERNEL_ITERATIONS = 1

    def image_file_exists(self, filename):
        return os.path.isfile(filename)

    def read_image_as_grasycale(self, filename):
        self.image = cv2.imread(filename, self.GRAYSCALE_INPUT)
        return self.image

    def apply_median_blur(self):
        self.image = cv2.medianBlur(self.image, self.MEDIAN_BLUR_KERNAL_SIZE)
        return self.image

    def apply_adaptive_threshold(self):
        self.threshold_image = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 15, 2)
        return self.threshold_image

    def copy_image(self, image):
        return image.copy()

    def get_shape_info(self, image):
        return image.shape

    def get_structuring_element(self, height, width):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (height,width))
        return kernel

    def erode_image(self, image, kernel_size):
        return cv2.erode(image,kernel_size,iterations = self.KERNEL_ITERATIONS)

    def dilate_image(self, image, kernel_size):
        return cv2.dilate(image,kernel_size,iterations = self.KERNEL_ITERATIONS)

    def create_empty_mask(self, row, column):
        """
        Reference material http://stackoverflow.com/questions/16235955/create-a-multichannel-zeros-mat-in-python-with-cv2
        """
        return np.zeros((row,column),np.uint8)

    def convert_black_threshold_to_white(self, image):
        self.threshold_image[np.where(image == 255)] = 0
        return self.threshold_image

    def convert_white_to_black(self, image, blank_mask):
        """
         Found a better way to itterate over the image http://stackoverflow.com/questions/30331944/finding-red-color-using-python-opencv
        """
        blank_mask[np.where(self.threshold_image == 0)] = 255
        return blank_mask

    def create_kernels_of_ones(self, height, width):
        return np.ones((height,width),np.uint8)

    def find_contours_in_mask(self, mask):
        """
        About unpacking the variables some issue it didn't work some times http://stackoverflow.com/questions/25504964/opencv-python-valueerror-too-many-values-to-unpack
        """
        contour_info = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contour_info[1]
        return contour_info

    def draw_contours(self, mask):
        cv2.drawContours(mask,self.contours, -1, (255, 0, 0), thickness=cv2.FILLED)
        return mask

    def prepare_image_to_save(self, image_file):
        filename, file_extension = os.path.splitext(image_file)
        self.image_path = "{0}.tif".format(filename)
        return self.image_path

    def save_image(self, image):
        cv2.imwrite(self.image_path, image)
