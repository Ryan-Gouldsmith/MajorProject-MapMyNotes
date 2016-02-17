#!/usr/bin/python
import unittest
import sys
import pytest

import os

import test_training_blue.scripts.blueline_adaptive_threshold as blueline

class TestBlueLinedAdaptedThreshold(object):
    def setup(self):
        self.threshold = blueline.Blueline_Adaptive_Threshold()
        self.image_file = "test_script/test_image.jpg"

    def test_image_exists(self):
        assert True == self.threshold.image_file_exists(self.image_file)

    def test_image_doesnot_exist(self):
        false_file = "/test_script/false_image.jpg"
        assert False == self.threshold.image_file_exists(false_file)

    def test_reading_image(self):
        assert None is not self.threshold.read_image(self.image_file)

    def test_grayscale_is_an_array(self):
        grayscale_image = self.threshold.read_image(self.image_file)

        assert len(grayscale_image) is not 0

    def test_convert_to_grayscale(self):

        
