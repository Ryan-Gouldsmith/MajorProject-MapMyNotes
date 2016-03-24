import pytest
from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.exifparser import ExifParser
class TestExifParsing(object):

    def setup(self):
        self.app = application.test_client()
        self.file_test_upload_path = "MapMyNotesApplication/upload/test2.jpg"

    def test_returns_correct_exif_data(self):
        parser = ExifParser(self.file_test_upload_path)

        exif_data = parser.parse_exif()

        assert type(exif_data) == dict

    def test_return_correct_date_for_image_taken(self):
        parser = ExifParser(self.file_test_upload_path)
        exif_data = parser.parse_exif()
        start_date = parser.get_image_date()

        assert start_date == '2016:01:31 13:47:14'
