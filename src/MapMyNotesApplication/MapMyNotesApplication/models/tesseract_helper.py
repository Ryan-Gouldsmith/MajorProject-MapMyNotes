from tesserocr import PyTessBaseAPI, RIL


class TesseractHelper(object):

    CUSTOM_LANGUAGE = "eng.ryan.exp2a"

    def __init__(self):
        self.tesseract_api = PyTessBaseAPI(lang=self.CUSTOM_LANGUAGE)

    def get_custom_language(self):
        return self.tesseract_api.GetInitLanguagesAsString()

    def set_image(self, image):
        self.image = image

    def set_tiff_image_for_analysis(self, image):
        self.tesseract_api.SetImageFile(image)

    def get_confidence_and_words_from_image(self):
        # Off the readME, testing it out to see if I can get the confidence levels of every word in a line https://github.com/sirfz/tesserocr
        boxes = self.tesseract_api.GetComponentImages(RIL.TEXTLINE, True)
        print 'Found {} textline image components.'.format(len(boxes))
        for i, (im, box, _, _) in enumerate(boxes):
            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            self.tesseract_api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            ocrResult = self.tesseract_api.GetUTF8Text()
            conf = self.tesseract_api.MeanTextConf()
            print self.tesseract_api.MapWordConfidences()
            print (u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
               "confidence: {1}, text: {2}").format(i, conf, ocrResult, **box)
        return self.tesseract_api.MapWordConfidences()
