#!/usr/bin/python

import os

class Blueline_Adaptive_Threshold(object):

    def image_file_exists(self, filename):
        # Going up a directory http://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
        script_root = os.path.dirname(os.path.dirname(__file__))
        return os.path.isfile(os.path.join(script_root, filename))





if __name__ == "__main__":

    true_or_false = image_file_exists("foo")

# Take an image from the input and convert it to grayscale

# perform smoothing and run threshold

# save the image
