import cv2
import numpy as np
import os
import sys

image = cv2.imread(sys.argv[1], 0)

#http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
filename, file_extension = os.path.splitext(sys.argv[1])
path = "images/grayscale_" +filename + ".tiff"
cv2.imwrite(path, image)
