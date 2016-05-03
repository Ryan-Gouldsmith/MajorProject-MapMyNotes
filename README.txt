# ReadMe TextFile for MapMyNotes

The following explains the location of the technical work:

## Web application
The following discusses the structure of the application for the web application:

- src/ contains the the web component of the MapMyNotes application

### Tests for the web application
Tests are located in the directory:
- src/
    MapMyNotesApplication/
      tests/

Inside the the test directory there is a mock data directory which some mock data has been included for the testing.
Integration tests are prefixed: test_integration_x.py
Acceptance tests are prefixed: test_acceptance_y.py
Unit tests are prefixed: test_class

To run the testing suite run the script, from the current directory,  ./test_flask.sh to run all the tests.


### Source code for the web application
The source code for the application is linked throughout the directory:
- src/
    MapMyNotesApplication/

All controllers, models and views are located in the appropriate directorier under:
- src/
    MapMyNotesApplication/
      MapMyNotesApplication/

### Source code for the image segmentation
To view the source code for the image segmentation go to the directory:
- tesseract_training_data/
    tesseract_training_on_adaptive_threshold/
      binarise_image.py.

Addtionally all image segmentation test images and Tesseract test images are in the directory:
- tesseract_training_data/
    tesseract_training_on_adaptive_threshold/

All normal images are test images for the segmentation but the tiff images are used for the Tesseract handwriting training examples.

### Tesseract training results
The results are in the directory:
- tesseract_training_data/
    tesseract_training_on_adaptive_threshold/

All stat images are in the eng.ryan.expVersion_stat.txt.

# Installing the application and dependencies
The application needs to have a series of dependencies to be created before being included.

The .travis yml file shows the installation script on Ubuntu.

# REFERENCE For Open CV build scripts: http://stackoverflow.com/questions/15790501/why-cv2-so-missing-after-opencv-installed and http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/

# REFERENCE Compiling tesseract from source: https://github.com/tesseract-ocr/tesseract/wiki/Compiling

# Reference Leptonica Build script: http://www.leptonica.org/source/README.html
to install:
  - sudo apt-get install -y libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
  - sudo apt-get install -y python-dev python-numpy
  - sudo apt-get install -y autoconf automake libtool
  - sudo apt-get install -y libpng12-dev
  - sudo apt-get install -y libjpeg62-dev
  - sudo apt-get install -y libtiff4-dev
  - sudo apt-get install -y zlib1g-dev
  - wget http://www.leptonica.org/source/leptonica-1.73.tar.gz
  - tar xzvf leptonica-1.73.tar.gz
  - cd leptonica-1.73
  - ./configure
  - make
  - sudo make install
  - cd ../
  - git clone https://github.com/tesseract-ocr/tesseract.git
  - cd tesseract
  - ./autogen.sh
  - ./configure
  - LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make
  - sudo make install
  - sudo ldconfig
  - cd ../
  - git clone https://github.com/Itseez/opencv.git
  - cd opencv
  - git checkout 3.0.0
  - mkdir build
  - cd build
  - cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..
  - make -j4
  - sudo make install
  - export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
  - cd ../../
  - "pip install -r requirements.txt"
  - sudo cp tesseract_training_data/tesseract_training_on_adaptive_threshold/eng.ryan.exp2a.traineddata /usr/local/share/tessdata

After the following have been completed, change to the /src/MapMyNotesApplication/ and run: python run.py

This will now load the file at localhost:5000 proceed to use the examples to attempt to use the application.
