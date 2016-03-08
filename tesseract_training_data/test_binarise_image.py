#!/usr/bin/python
import unittest
import sys
import pytest
import cv2
import os
import numpy as np

import tesseract_training_on_adaptive_threshold.binarise_image as blueline

class TestBlueLinedAdaptedThreshold(object):
    def setup(self):
        self.threshold = blueline.BinariseImage()
        self.image_file = "test_script/test_image.jpg"



    def test_image_exists(self):
        assert self.threshold.image_file_exists(self.image_file) is True

    def test_image_doesnot_exist(self):
        false_file = "/test_script/false_image.jpg"

        assert self.threshold.image_file_exists(false_file) is False

    def test_reading_image_as_grayscale(self):
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        image_attributes = read_in_image.shape
        #http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html Found it returns a tuple containing 2 attributes. So to make it grayscale it should not have 3 like normal colour.
        assert len(image_attributes) is 2

    def test_reading_image_as_grayscale_returns_image_not_none(self):
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        assert read_in_image is not None

    def test_add_median_blur_to_image_alters_the_image(self):
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        assert median_blurred_image is not read_in_image

    def test_converting_median_blurred_image_to_adaptive_threshold(self):
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        assert median_blurred_image is not self.threshold.apply_adaptive_threshold()

    def test_copying_theshold_images(self):
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        copied_threshold_image = self.threshold.copy_image(threshold_image)

        assert np.array_equal(threshold_image, copied_threshold_image) is True

    def test_should_return_the_information_about_a_shape_as_tuple(self):
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        lines = self.threshold.copy_image(threshold_image)

        assert len(self.threshold.get_shape_info(lines)) is 2

    def test_get_structing_elements(self):
        width = 75
        height = 1
        structuring_element = self.threshold.get_structuring_element(width, height)

        assert len(structuring_element[0]) is 75

    def test_erode_image(self):
        width = 75
        height = 1
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        lines = self.threshold.copy_image(threshold_image)
        kernal_structure = self.threshold.get_structuring_element(width, height)

        eroded_image = self.threshold.erode_image(lines, kernal_structure)

        assert lines is not eroded_image

    def test_dilate_image(self):
        width = 75
        height = 1
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        lines = self.threshold.copy_image(threshold_image)
        kernal_structure = self.threshold.get_structuring_element(width, height)

        dilated_image = self.threshold.dilate_image(lines, kernal_structure)

        assert lines is not dilated_image

    def test_creating_blank_image_array(self):
        row_value = 100
        column_value = 100
        empty_mask = self.threshold.create_empty_mask(row_value, column_value)

        assert len(empty_mask[0]) is 100

    def convert_black_characters_to_white(self):

        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        lines = self.threshold.copy_image(threshold_image)

        dilated_image = self.threshold.dilate_image(lines, kernal_structure)

        new_mask = self.threshold.convert_black_threshold_to_white(dilated_image)

        black_array = mask[np.where(mask == 255)]

        assert len(black_array) == 0

    def test_black_characters_are_on_blank_image(self):
        width = 75
        height = 1
        read_in_image = self.threshold.read_image_as_grasycale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()


        lines = self.threshold.copy_image(threshold_image)
        kernal_structure = self.threshold.get_structuring_element(width, height)

        dilated_image = self.threshold.dilate_image(lines, kernal_structure)
        new_mask = self.threshold.convert_black_threshold_to_white(dilated_image)

        row_value = 100
        column_value = 100
        empty_mask = self.threshold.create_empty_mask(row_value, column_value)

        mask = self.threshold.convert_white_to_black(new_mask, empty_mask)

        # gets the black values and checks that it has converted some.
        black_array = mask[np.where(mask == 255)]

        assert len(black_array) > 0

    def test_creating_a_1x1_kernel(self):
        height = 3
        width = 3
        kernel = self.threshold.create_kernels_of_ones(height, width)

        assert len(kernel[0]) == 3





    """


    def test_get_kernel_type(self):
        kernel = self.threshold.get_kernel(2)

        # Is instance stuff http://stackoverflow.com/questions/12569452/how-to-identify-numpy-types-in-python
        assert isinstance(kernel, np.ndarray) is True

    def test_erroding_image(self):
        image = cv2.imread(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        assert eroding_image is not None

    def test_black_text_extraction(self):
        image = cv2.imread(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        assert self.threshold.black_text_extraction(eroding_image) is not None

    def test_get_image_dimensions(self):
        image = cv2.imread(self.image_file)
        image_height, image_width, image_depth = image.shape
        test_dimensions = (image_height, image_width, image_depth)

        self.threshold.read_image(self.image_file)

        assert test_dimensions == (self.threshold.get_image_dimensions())

    def test_get_blank_mask(self):
        image = cv2.imread(self.image_file)
        image_height, image_width, image_depth = image.shape
        image_mask = np.zeros((image_height, image_width),np.uint8)

        self.threshold.read_image(self.image_file)

        # checks to see all the values are the same
        assert image_mask.all() == self.threshold.get_blank_image_mask().all()

    def test_convert_text_extraction_to_mask(self):
        image = self.threshold.read_image(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        mask = self.threshold.get_blank_image_mask()
        black_text = self.threshold.black_text_extraction(eroding_image)

        mask = self.threshold.convert_text_extraction_to_mask()

        # gets the black values and checks that it has converted some.
        black_array = mask[np.where(mask == 255)]

        assert len(black_array) > 0


    def test_apply_adaptive_threshold_to_image(self):
        image = self.threshold.read_image(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        mask = self.threshold.get_blank_image_mask()
        black_text = self.threshold.black_text_extraction(eroding_image)

        kernel = self.threshold.get_kernel(5)
        eroding_image = self.threshold.erode_image(black_text, kernel)

        mask = self.threshold.convert_text_extraction_to_mask()

        threshold_image = self.threshold.apply_threshold(mask)

        assert threshold_image is not None

    def test_saves_new_tiff_image(self):
        image = self.threshold.read_image(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        mask = self.threshold.get_blank_image_mask()
        black_text = self.threshold.black_text_extraction(eroding_image)

        kernel = self.threshold.get_kernel(5)
        eroding_image = self.threshold.erode_image(black_text, kernel)

        mask = self.threshold.convert_text_extraction_to_mask()

        threshold_image = self.threshold.apply_threshold(mask)

        threshold_image = self.threshold.apply_threshold(mask)

        self.threshold.save_adaptive_threshold_image(self.image_file)

        test_root = os.path.dirname(__file__)

        filename = "test_image.tiff"

        assert True is os.path.isfile(os.path.join(test_root, filename))
    """
