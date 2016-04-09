from tesserocr import PyTessBaseAPI

from MapMyNotesApplication import database
from MapMyNotesApplication.models.tesseract_helper import TesseractHelper
from flask import Flask
from flask.ext.testing import TestCase


class TestTesseractHelper(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        """
        http://blog.toast38coza.me/adding-a-database-to-a-flask-app/
        Used to help with the test database, could move this to a config file.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        self.image = "MapMyNotesApplication/upload/test.tif"
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_creation_of_helper_returns_py_tess_base_api_instance(self):
        tesseract_helper = TesseractHelper(self.image)
        assert type(tesseract_helper.tesseract_api) is PyTessBaseAPI

    def test_default_language_is_custom_language(self):
        tesseract_helper = TesseractHelper(self.image)
        assert tesseract_helper.tesseract_api.GetInitLanguagesAsString() == 'eng.ryan.exp2a'

    def test_setting_image_to_be_used_for_recognition(self):
        tesseract_helper = TesseractHelper(self.image)
        assert tesseract_helper.image == self.image

    def test_setting_tesseract_image_for_analysis(self):
        """ Reference:
         http://stackoverflow.com/questions/4319825/python-unittest-opposite-of-assertraises
        """
        try:
            tesseract_helper = TesseractHelper(self.image)
            tesseract_helper.set_tiff_image_for_analysis()
        except RuntimeError:
            self.fail()

    def test_should_raise_exception_bad_image_file(self):
        tesseract_helper = TesseractHelper("foo")
        self.assertRaises(RuntimeError, tesseract_helper.set_tiff_image_for_analysis)

    def test_getting_confidence_should_return_list_of_tuples(self):
        tesseract_helper = TesseractHelper(self.image)
        tesseract_helper.set_tiff_image_for_analysis()
        tuples = tesseract_helper.get_confidence_and_words_from_image()
        assert type(tuples) is list
        assert type(tuples[0][0]) is tuple
