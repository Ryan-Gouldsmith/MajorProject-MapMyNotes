import cv2
import numpy as np
import copy
import sys
import os

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
        return np.zeros((row,column),np.uint8)

    def convert_black_threshold_to_white(self, image):
        self.threshold_image[np.where(image == 255)] = 0
        return self.threshold_image

    def convert_white_to_black(self, image, blank_mask):
        blank_mask[np.where(self.threshold_image == 0)] = 255
        return blank_mask

    def create_kernels_of_ones(self, height, width):
        return np.ones((height,width),np.uint8)

    def find_contours_in_mask(self, mask):
        contour_info = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contour_info[1]
        return contour_info

    def draw_contours(self, mask):
        cv2.drawContours(mask,self.contours,-1,(255,0,0),thickness=cv2.FILLED)
        return mask

    def prepare_image_to_save(self, image_file):
        filename, file_extension = os.path.splitext(image_file)
        self.image_path = "{0}.tiff".format(filename)
        return self.image_path

    def save_image(self, image):
        cv2.imwrite(self.image_path, image)

if __name__ == "__main__":
    binarise = BinariseImage()
    if binarise.image_file_exists(sys.argv[1]):

        image = binarise.read_image_as_grasycale(sys.argv[1])
        image = binarise.apply_median_blur()
        threshold_image = binarise.apply_adaptive_threshold()
        horizontal_lines = binarise.copy_image(threshold_image)
        rows, columns = binarise.get_shape_info(horizontal_lines)
        structuring_element_kernel = binarise.get_structuring_element(75,1)
        horizontal_lines = binarise.erode_image(horizontal_lines, structuring_element_kernel)
        horizontal_lines = binarise.dilate_image(horizontal_lines, structuring_element_kernel)
        #Thats the morphological dilatate?
        horizontal_lines = binarise.dilate_image(horizontal_lines, structuring_element_kernel)

        modified_threshold_mask = binarise.convert_black_threshold_to_white(horizontal_lines)

        new_mask = binarise.create_empty_mask(rows, columns)

        black_text_mask = binarise.convert_white_to_black(modified_threshold_mask, new_mask)

        one_kernel = binarise.create_kernels_of_ones(3,3)

        dilated_black_text_mask = binarise.dilate_image(black_text_mask, one_kernel)

        image, contours, approximation = binarise.find_contours_in_mask(dilated_black_text_mask)

        dilated_black_text_mask = binarise.draw_contours(dilated_black_text_mask)

        ones_kernel = binarise.create_kernels_of_ones(7,7)

        final_output = binarise.erode_image(dilated_black_text_mask, ones_kernel)

        path = binarise.prepare_image_to_save(sys.argv[1])

        cv2.imshow("im", final_output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        binarise.save_image(final_output)

    else:
        print "File doesn't exist sorry"
