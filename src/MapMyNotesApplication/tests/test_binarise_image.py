#!/usr/bin/python
import os

import MapMyNotesApplication.models.binarise_image as blueline
import numpy as np


class TestBlueLinedAdaptedThreshold(object):
    def setup(self):
        self.threshold = blueline.BinariseImage()
        self.image_file = "tests/test_image.jpg"

    def teardown(self):
        if os.path.isfile("tests/test_image.tif"):
            os.remove("tests/test_image.tif")

    def test_image_exists(self):
        assert self.threshold.image_file_exists(self.image_file) is True

    def test_image_does_not_exist(self):
        false_file = "/test_script/false_image.jpg"

        assert self.threshold.image_file_exists(false_file) is False

    def test_reading_image_as_grayscale(self):
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        image_attributes = read_in_image.shape
        # http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html Found it returns a tuple containing 2 attributes. So to make it grayscale it should not have 3 like normal colour.
        assert len(image_attributes) is 2

    def test_reading_image_as_grayscale_returns_image_not_none(self):
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        assert read_in_image is not None

    def test_add_median_blur_to_image_alters_the_image(self):
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        assert median_blurred_image is not read_in_image

    def test_converting_median_blurred_image_to_adaptive_threshold(self):
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        assert median_blurred_image is not self.threshold.apply_adaptive_threshold()

    def test_copying_theshold_images(self):
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        copied_threshold_image = self.threshold.copy_image(threshold_image)

        assert np.array_equal(threshold_image, copied_threshold_image) is True

    def test_should_return_the_information_about_a_shape_as_tuple(self):
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

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
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        lines = self.threshold.copy_image(threshold_image)
        kernal_structure = self.threshold.get_structuring_element(width, height)

        eroded_image = self.threshold.erode_image(lines, kernal_structure)

        assert lines is not eroded_image

    def test_dilate_image(self):
        width = 75
        height = 1
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

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
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

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
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        lines = self.threshold.copy_image(threshold_image)
        kernal_structure = self.threshold.get_structuring_element(width, height)

        dilated_image = self.threshold.dilate_image(lines, kernal_structure)
        new_mask = self.threshold.convert_black_threshold_to_white(dilated_image)

        row_value, column_value = self.threshold.get_shape_info(lines)
        empty_mask = self.threshold.create_empty_mask(row_value, column_value)

        mask = self.threshold.convert_white_to_black(empty_mask)

        # gets the black values and checks that it has converted some.
        # Found a better way than itterating over the whole pixels http://stackoverflow.com/questions/30331944/finding-red-color-using-python-opencv
        black_array = mask[np.where(mask == 255)]

        assert len(black_array) > 0

    def test_creating_a_1x1_kernel(self):
        height = 3
        width = 3
        kernel = self.threshold.create_kernels_of_ones(height, width)

        assert len(kernel[0]) == 3

    def test_finding_contours_of_mask_return_tuple(self):
        width = 75
        height = 1
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()

        threshold_image = self.threshold.apply_adaptive_threshold()

        lines = self.threshold.copy_image(threshold_image)
        kernal_structure = self.threshold.get_structuring_element(width, height)

        dilated_image = self.threshold.dilate_image(lines, kernal_structure)
        new_mask = self.threshold.convert_black_threshold_to_white(dilated_image)

        row_value, column_value = self.threshold.get_shape_info(lines)
        empty_mask = self.threshold.create_empty_mask(row_value, column_value)

        mask = self.threshold.convert_white_to_black(empty_mask)

        tuple_contour_info = self.threshold.find_contours_in_mask(mask)

        assert len(tuple_contour_info) == 3

        assert type(tuple_contour_info[1]) is list

    def test_drawing_on_contour_to_mask(self):
        width = 75
        height = 1
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)

        median_blurred_image = self.threshold.apply_median_blur()
        threshold_image = self.threshold.apply_adaptive_threshold()
        lines = self.threshold.copy_image(threshold_image)
        kernal_structure = self.threshold.get_structuring_element(width, height)

        dilated_image = self.threshold.dilate_image(lines, kernal_structure)
        new_mask = self.threshold.convert_black_threshold_to_white(dilated_image)

        row_value, column_value = self.threshold.get_shape_info(lines)
        empty_mask = self.threshold.create_empty_mask(row_value, column_value)

        mask = self.threshold.convert_white_to_black(empty_mask)

        tuple_contour_info = self.threshold.find_contours_in_mask(mask)

        returned_mask_with_contours = self.threshold.draw_contours(mask)

        assert returned_mask_with_contours is not tuple_contour_info

    def test_prepare_tiff_file_for_saving(self):
        returned_tiff_file = self.threshold.prepare_image_to_save(self.image_file)

        assert returned_tiff_file == "tests/test_image.tif"

    def test_saving_image_file_to_filestore(self):
        read_in_image = self.threshold.read_image_as_grayscale(self.image_file)
        image = self.threshold.apply_median_blur()

        returned_tiff_file = self.threshold.prepare_image_to_save(self.image_file)

        self.threshold.save_image(image)

        assert os.path.isfile('tests/test_image.tif') is True
