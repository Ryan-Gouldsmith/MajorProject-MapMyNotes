import cv2
import numpy as np
import copy
import sys
import os

"""
REFERENCE Ideas considered from, but changed it to match the lines of my own text
http://stackoverflow.com/questions/10196198/how-to-remove-convexity-defects-in-a-sudoku-square
Excellent resource for extracting lines from music notes. Used for guidance on different sections of this script.
Modified extensively and used connected components to extract the text.
http://docs.opencv.org/3.1.0/d1/dee/tutorial_moprh_lines_detection.html#gsc.tab=0

Built upon the work completed which analysed that adaptive threshold would be good.
"""


class BinariseImage(object):
    GRAYSCALE_INPUT = 0
    MEDIAN_BLUR_KERNEL_SIZE = 7
    KERNEL_ITERATIONS = 1

    def __init__(self):
        """
        Creates a new binarisation instance
        """
        self.image = None
        self.threshold_image = None
        self.contours = None
        self.image_path = None

    def image_file_exists(self, filename):
        """
        Checks to see if the filename exists
        Parameters
        ----------
        filename: String representation of the filename which has been used for binaristion.

        Returns
        -------
        True if the file exists
        False if the file does not exist
        """
        return os.path.isfile(filename)

    def read_image_as_grayscale(self, filename):
        """
        Converts the image to grayscale after reading it in.
        Parameters
        ----------
        filename: The image that will be read and converted to grayscale

        Returns
        -------
        The grayscale image
        """
        self.image = cv2.imread(filename, self.GRAYSCALE_INPUT)
        return self.image

    def apply_median_blur(self):
        """
        Uses the median blur API to attempt to blur the image a little prior to the binarisation
        Returns
        -------
        A blurred image
        """
        self.image = cv2.medianBlur(self.image, self.MEDIAN_BLUR_KERNEL_SIZE)
        return self.image

    def apply_adaptive_threshold(self):
        """
        Applies an adaptive threshold onto the image, using a Gaussian
        Returns
        -------
        The threshold image
        """
        # http://docs.opencv.org/3.1.0/d7/d4d/tutorial_py_thresholding.html#gsc.tab=0
        self.threshold_image = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY_INV, 15, 2)
        return self.threshold_image

    def copy_image(self, image):
        """
        Copies an image so the modification do not happen on the old image
        Parameters
        ----------
        image: The image to be copied

        Returns
        -------
        A new copy.
        """
        return image.copy()

    def get_shape_info(self, image):
        """
        Gets the shape information about the image such as the row and column size of the image.
        Parameters
        ----------
        image: The image which will be copied from the shape

        Returns
        -------

        """
        return image.shape

    def get_structuring_element(self, height, width):
        """
        Gets the structuring elements from the image. To extract the rectangular shapes from the image, i.e the lines
        Parameters
        ----------
        height: Height of the kernel size
        width: Width of the kernel size

        Returns
        -------
        The structuring element kernel.
        """
        # http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (height, width))
        return kernel

    def erode_image(self, image, kernel_size):
        """
        Performs erosion on the image to attempt to reduce the noise pixels.
        Parameters
        ----------
        image: The image which will be eroded.
        kernel_size: The kernel size that will erode

        Returns
        -------
        An eroded image.
        """
        return cv2.erode(image, kernel_size, iterations=self.KERNEL_ITERATIONS)

    def dilate_image(self, image, kernel_size):
        """
        Performs dilation over an image. Making the text thicker and the white thinner
        Parameters
        ----------
        image: The image which will be dilated
        kernel_size: The Kernel size which the image will dilate

        Returns
        -------
        A dilated image
        """
        return cv2.dilate(image, kernel_size, iterations=self.KERNEL_ITERATIONS)



    def create_empty_mask(self, row, column):
        """
        Create an empty numpy array based on the row and column size of an image
        Parameters
        ----------
        row: int - the row size
        column: int - column size

        Returns
        -------
        A Numpy Array of zeros based on the row and column size.
        """
        """Reference material
            http://stackoverflow.com/questions/16235955/create-a-multichannel-zeros-mat-in-python-with-cv2
        """
        return np.zeros((row, column), np.uint8)

    def convert_black_threshold_to_white(self, image):
        """
        Converts all black text to white text using numpy arrayss
        Parameters
        ----------
        image: The image  with black pixels

        Returns
        -------
        A threshold image which has no black pixels
        """

        """
            Found a better way to iterate over the image - wanted to do it more efficiently than a for loop.
            http://stackoverflow.com/questions/30331944/finding-red-color-using-python-opencv
        """
        self.threshold_image[np.where(image == 255)] = 0
        return self.threshold_image



    def convert_white_to_black(self, blank_mask):
        """
        Converts the white pixels to black in the image
        Parameters
        ----------
        blank_mask: Array of empty pixels

        Returns
        -------
        An image which has no white pixels only black.
        """
        blank_mask[np.where(self.threshold_image == 0)] = 255
        return blank_mask

    def create_kernels_of_ones(self, height, width):
        """
        Create a kernel of ones using Numpy Array
        Parameters
        ----------
        height: the height of the kernel
        width: Width of the kernel.

        Returns
        -------
        A Numpy array of ones.
        """
        return np.ones((height, width), np.uint8)



    def find_contours_in_mask(self, mask):
        """
        Find all given contours in the mask to extract any text from the image.
        Parameters
        ----------
        mask: The numpy array which will be extracted from the contours.

        Returns
        -------
        All contour information
        """

        """
            This differs from the original OpenCV guide as it attempt to extract connected components.
            About unpacking the variables some issue it didn't work some times
            Thought that since the pixels would be connected then
            http://stackoverflow.com/questions/25504964/opencv-python-valueerror-too-many-values-to-unpack

            This didn't give me a good result, so the comment by William on
            http://stackoverflow.com/questions/23506105/extracting-text-opencv gave me the idea of contours as
            the image pixels will be connected. So further  investigations into Python's contour API
            http://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html#gsc.tab=0 was conducted.

            Reference guide too for contours.
            http://opencvpython.blogspot.co.uk/2012/06/hi-this-article-is-tutorial-which-try.html
        """
        contour_info = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # experimentation showed that  1 worked well.
        self.contours = contour_info[1]
        return contour_info

    def draw_contours(self, mask):
        """
        Drawing all the contours onto the mask - this essentially transfers all the text from the image onto the
        blank mask. Used filled so t
        Parameters
        ----------
        mask: A blank mask which will have the characters put onto it.

        Returns
        -------
        A binarised mask.
        """

        """
            Continuing drawing the all the contours.
            Filled changed in the new versions:
            http://stackoverflow.com/questions/15340052/python-opencv-cv2-equivalent-for-cv-filled
        """
        cv2.drawContours(mask, self.contours, -1, (255, 0, 0), thickness=cv2.FILLED)
        return mask

    def prepare_image_to_save(self, image_file):
        """
        Formats the file for a given filename including the tiff extension.

        Parameters
        ----------
        image_file: The image file which will be prepared to save to the filestore.

        Returns
        -------

        """
        filename, file_extension = os.path.splitext(image_file)
        self.image_path = "{0}.tif".format(filename)
        return self.image_path

    def save_image(self, image):
        """
        Uses OpenCV's write to save the image to filestore
        Parameters
        ----------
        image: The image which will be saved.
        """
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
