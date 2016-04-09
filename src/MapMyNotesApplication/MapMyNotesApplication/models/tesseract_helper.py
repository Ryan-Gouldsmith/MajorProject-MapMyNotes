from tesserocr import PyTessBaseAPI


class TesseractHelper(object):
    CUSTOM_LANGUAGE = "eng.ryan.exp2a"
    NUMBER_OF_LINES = 3

    def __init__(self, image):
        self.tesseract_api = PyTessBaseAPI(lang=self.CUSTOM_LANGUAGE)
        self.image = image

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

        return list_word_confidence
