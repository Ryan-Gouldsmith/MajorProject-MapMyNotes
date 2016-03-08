import cv2
import numpy as np
import copy
import sys
import os

class BinariseImage(object):

    GRAYSCALE_INPUT = 0
    MEDIAN_BLUR_KERNAL_SIZE = 7

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
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (75,1))
        return kernel

    def erode_image(self, image, kernel_size):
        return cv2.erode(image,kernel_size,iterations = 1)

    def dilate_image(self, image, kernel_size):
        return cv2.dilate(image,kernel_size,iterations = 1)

    def create_empty_mask(self, row, column):
        return np.zeros((row,column),np.uint8)

    def convert_black_threshold_to_white(self, image):
        white_mask = self.threshold_image[np.where(image == 255)] = 0
        return white_mask

    def convert_white_to_black(self, image, blank_mask):
        blank_mask[np.where(image == 0)] = 255
        return blank_mask

    def create_kernels_of_ones(self, height, width):
        return np.ones((3,3),np.uint8)
