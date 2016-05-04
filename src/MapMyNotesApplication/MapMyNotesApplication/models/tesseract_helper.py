from tesserocr import PyTessBaseAPI

"""
Integrates with the TesserOCR library
"""


class TesseractHelper(object):
    CUSTOM_LANGUAGE = "eng.ryan.exp2a"
    NUMBER_OF_LINES = 3

    def __init__(self, image):
        """
        Creates a new instance of the Tesseract helper
        Parameters
        ----------
        image: Sets the image which will be used for the text extraction.
        """
        self.tesseract_api = PyTessBaseAPI(lang=self.CUSTOM_LANGUAGE)
        self.image = image
        self.list_words_confidence = None

    def set_tiff_image_for_analysis(self):
        """
        Returns
        -------
        Sets the image to be the file for the tesserocr library
        """
        self.tesseract_api.SetImageFile(self.image)

    def get_confidence_and_words_from_image(self):
        """
        Extracts the text lines from the image - then loops over them sets the bounding boxes and returns all the
        confidence scores.

        Returns
        -------
        A list of the confidence values for each word
        """

        """
            Modified from the Advanced API interaction on the ReadMe.
            Further referencing from the source code. https://github.com/sirfz/tesserocr
         """
        # gets the textlines like Tesseract does from the image
        text_boxes = self.tesseract_api.GetTextlines(True)
        list_word_confidence = []

        # We only want the first few lines for the meta-data, so let's use list comprehensions to get the lines.
        for (image, bounding_box, block_id, paragraph_id) in text_boxes[:self.NUMBER_OF_LINES]:
            # You have to set the bounding box so that we know which line we are on.
            # so we can get the text and confidence as tuple values.
            # Otherwise GetUTF8Text returns all the text again, not what we want.
            self.tesseract_api.SetRectangle(bounding_box['x'], bounding_box['y'], bounding_box['w'], bounding_box['h'])

            confidences = list(self.tesseract_api.MapWordConfidences())
            list_word_confidence.append(confidences)
        self.list_words_confidence = list_word_confidence
        return list_word_confidence

    def get_module_code_line(self):
        """
        Uses list comprehension to extract the first item from the list
        Returns
        -------
        The tuple from the the list of confidence scores
        None if there could be nothing found
        """
        if len(self.list_words_confidence) > 0 and len(self.list_words_confidence[0]) > 0:
            return self.list_words_confidence[0][0] if (self.list_words_confidence is not None) else ""
        else:
            return None

    def get_title_line(self):
        """
        Returns
        -------
        An Array of Tuples: the remaining tuples from the first array item after the index of one
        Empty list if there were no tuples
        """
        if len(self.list_words_confidence) > 0 and len(self.list_words_confidence[0][1:]) > 0:
            return self.list_words_confidence[0][1:] if (self.list_words_confidence is not None) else ""
        else:
            return []

    def get_date_line(self):
        """
        Returns
        -------
        An array of Tuples from the second index of the list confidence scores
        An empty list if there is no second index.
        """
        if len(self.list_words_confidence) > 1:
            return self.list_words_confidence[1] if (self.list_words_confidence is not None) else ""
        else:
            return []

    def get_lecturer_line(self):
        """
        Returns
        -------
        An array of Tuples from the third index of the list confidence scores
        An empty list if there is no third index.
        """
        if len(self.list_words_confidence) > 2:
            return self.list_words_confidence[2] if (self.list_words_confidence is not None) else ""
        else:
            return []
