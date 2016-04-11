from tesserocr import PyTessBaseAPI


class TesseractHelper(object):
    CUSTOM_LANGUAGE = "eng.ryan.exp2a"
    NUMBER_OF_LINES = 3

    def __init__(self, image):
        self.tesseract_api = PyTessBaseAPI(lang=self.CUSTOM_LANGUAGE)
        self.image = image
        self.list_words_confidence = None

    def set_tiff_image_for_analysis(self):
        self.tesseract_api.SetImageFile(self.image)

    """Modified from the Advanced API interaction on the ReadMe.
       Further referencing from the source code. https://github.com/sirfz/tesserocr
    """

    def get_confidence_and_words_from_image(self):
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
        return self.list_words_confidence[0][0] if (self.list_words_confidence is not None) else ""

    def get_title_line(self):
        return self.list_words_confidence[0][1:] if (self.list_words_confidence is not None) else ""

    def get_date_line(self):
        return self.list_words_confidence[1] if (self.list_words_confidence is not None) else ""

    def get_lecturer_line(self):
        return self.list_words_confidence[2] if (self.list_words_confidence is not None) else ""
