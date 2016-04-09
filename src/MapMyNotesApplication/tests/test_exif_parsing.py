from MapMyNotesApplication.models.exif_parser import ExifParser
from flask import Flask
from flask.ext.testing import TestCase


class TestExifParsing(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.file_test_upload_path = "MapMyNotesApplication/upload/ryan_test_1.jpg"
        self.file_test_upload_path = "MapMyNotesApplication/upload/test2.jpg"
        return app

    def test_returns_correct_exif_data(self):
        parser = ExifParser(self.file_test_upload_path)

        exif_data = parser.parse_exif()

        assert type(exif_data) == dict

    def test_return_correct_date_for_image_taken(self):
        parser = ExifParser(self.file_test_upload_path)
        exif_data = parser.parse_exif()
        start_date = parser.get_image_date()

        assert start_date == '2016:01:31 13:47:14'
