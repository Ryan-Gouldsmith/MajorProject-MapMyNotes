#!/usr/bin/python
import unittest
import sys
import pytest
import cv2
import os
import numpy as np

import test_training_blue.scripts.blueline_adaptive_threshold as blueline

class TestBlueLinedAdaptedThreshold(object):
    def setup(self):
        self.threshold = blueline.Blueline_Adaptive_Threshold()
        self.image_file = "test_script/test_image.jpg"

    def test_image_exists(self):
        assert self.threshold.image_file_exists(self.image_file) is True

    def test_image_doesnot_exist(self):
        false_file = "/test_script/false_image.jpg"

        assert self.threshold.image_file_exists(false_file) is False

    def test_reading_image(self):
        assert self.threshold.read_image(self.image_file) is not None

    def test_image_is_an_array(self):
        coloured_image = self.threshold.read_image(self.image_file)

        assert len(coloured_image) is not 0

    def test_convert_to_grayscale(self):
        image = cv2.imread(self.image_file)
        grayscale_image = self.threshold.convert_to_grayscale(image)

        assert grayscale_image is not None

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

        self.threshold.convert_text_extraction_to_mask()

        # has transfered the colour over to the array. TODO I don't think this test is acually good enough and it doesn't filter all the 255 like I thought the manual said.
        assert len(np.in1d(self.threshold.mask, 255)) > 0


    def test_apply_adaptive_threshold_to_image(self):
        image = self.threshold.read_image(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        mask = self.threshold.get_blank_image_mask()
        black_text = self.threshold.black_text_extraction(eroding_image)

        self.threshold.convert_text_extraction_to_mask()

        threshold_image = self.threshold.apply_threshold()

        assert threshold_image is not None

    def test_saves_new_tiff_image(self):
        image = self.threshold.read_image(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        mask = self.threshold.get_blank_image_mask()
        black_text = self.threshold.black_text_extraction(eroding_image)

        self.threshold.convert_text_extraction_to_mask()

        threshold_image = self.threshold.apply_threshold()

        self.threshold.save_adaptive_threshold_image(self.image_file)

        test_root = os.path.dirname(__file__)

        filename = "test_image.tiff"
        assert True is os.path.isfile(os.path.join(test_root, filename))
