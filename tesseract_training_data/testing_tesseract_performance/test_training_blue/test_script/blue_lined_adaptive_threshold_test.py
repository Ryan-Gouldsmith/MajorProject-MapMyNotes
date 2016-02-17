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

    def test_grayscale_is_an_array(self):
        coloured_image = self.threshold.read_image(self.image_file)

        assert len(coloured_image) is not 0

    def test_convert_to_grayscale(self):
        image = cv2.imread(self.image_file)
        grayscale_image = self.threshold.convert_to_grayscale(image)

        assert grayscale_image is not None

    def test_get_kernel_type(self):
        kernel = self.threshold.get_kernel(2)

        assert isinstance(kernel, np.ndarray) is True

    def test_erroding_image(self):
        image = cv2.imread(self.image_file)
        greyscale_image = self.threshold.convert_to_grayscale(image)
        kernel = self.threshold.get_kernel(2)

        eroding_image = self.threshold.erode_image(greyscale_image, kernel)

        assert eroding_image is not None
