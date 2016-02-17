#!/usr/bin/python
import unittest
import sys
import pytest

import os

import test_training_blue.scripts.blueline_adaptive_threshold as blueline

class TestBlueLinedAdaptedThreshold(object):
    def setup(self):
        self.threshold = blueline.Blueline_Adaptive_Threshold()
        self.file_exists = "test_script/test_image.jpg"

    def test_image_exists(self):
        assert True == self.threshold.image_file_exists(self.file_exists)

    def test_image_doesnot_exist(self):
        false_file = "/test_script/false_image.jpg"
        assert False == self.threshold.image_file_exists(false_file)
