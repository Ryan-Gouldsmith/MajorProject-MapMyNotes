import os

from flask import Flask
from flask.ext.testing import TestCase
from mock import mock
from werkzeug.datastructures import FileStorage

from MapMyNotesApplication.models.file_upload_service import FileUploadService


class TestFileUploadService(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.file_test_upload_path = "MapMyNotesApplication/upload/ryan_test_1.jpg"
        return app

    def setUp(self):
        self.filename = "tests/ryan_test_1.jpg"
        self.file_upload_service = FileUploadService(self.filename)

        self.current_time_patch = mock.patch.object(FileUploadService, 'get_current_time')
        self.current_time_mock = self.current_time_patch.start()
        self.current_time_mock.return_value = "11111.1"

    def tearDown(self):
        if os.path.isfile(self.file_test_upload_path):
            os.remove(self.file_test_upload_path)

        mock.patch.stopall()

    def test_file_upload_with_slash(self):
        expected = self.file_upload_service.is_forward_slash_in_filename()

        assert expected is True

    def test_file_upload_without_slash(self):
        filename = "file.jpg"
        file_upload_service = FileUploadService(filename)
        expected = file_upload_service.is_forward_slash_in_filename()

        assert expected is False

    def test_prepare_file_path_file(self):
        self.file_upload_service.remove_slash_from_filename()
        expected = "ryan_test_1.jpg"

        assert self.file_upload_service.filename == expected

    def test_prepare_file_path_file_check_slash(self):
        self.file_upload_service.remove_slash_from_filename()

        assert "/" not in self.file_upload_service.filename

    def test_saving_a_filename_to_uploads(self):
        upload_directory = "MapMyNotesApplication/upload/"
        filename = "tests/ryan_test_1.jpg"
        file_object = open(filename, 'r')
        file_upload_service = FileUploadService(filename)
        # Found out I can use the File Storage object to mock the File used in the controller for Flask http://stackoverflow.com/questions/18249949/python-file-object-to-flasks-filestorage
        file = FileStorage(file_object)
        file_upload_service.remove_slash_from_filename()
        prepared_filename = file_upload_service.filename
        expected_file = upload_directory + prepared_filename
        file_upload_service.add_full_path_to_filename(upload_directory)
        file_upload_service.save_users_file(file)

        assert os.path.isfile(expected_file) is True

    def test_only_allow_uploading_of_images(self):
        filename = "tests/ryan_test_1.jpg"
        file_object = open(filename, 'r')
        file = FileStorage(file_object)
        file_upload_service = FileUploadService(filename)
        accepted_file_extension = file_upload_service.accepted_file_extension()

        assert accepted_file_extension is True

    def test_not_allow_uploading_of_images(self):
        filename = "tests/ryan_test_1.pdf"
        file_object = open(filename, 'r')
        file = FileStorage(file_object)
        file_upload_service = FileUploadService(filename)
        accepted_file_extension = file_upload_service.accepted_file_extension()

        assert accepted_file_extension is False

    def test_file_exists_fake_file(self):
        filename = "tests/fakefile.jpg"
        file_upload_service = FileUploadService(filename)
        file_upload_service.remove_slash_from_filename()
        file_upload_service.add_full_path_to_filename("tests/")
        file_exists = file_upload_service.file_exists()

        assert file_exists is False

    def test_file_exists_true_file(self):
        self.file_upload_service.remove_slash_from_filename()
        self.file_upload_service.add_full_path_to_filename("tests/")
        file_exists = self.file_upload_service.file_exists()

        assert file_exists is True

    def test_is_png_method_returns_true_when_its_a_png(self):
        filename = 'tests/test.png'
        file_upload_service = FileUploadService(filename)
        file_png = file_upload_service.is_png()

        assert file_png is True

    def test_is_png_method_returns_false_when_jpg(self):
        file_jpg = self.file_upload_service.is_png()

        assert file_jpg is False

    def test_add_full_path_to_filename_adds_the_correct_string(self):
        self.file_upload_service.remove_slash_from_filename()
        self.file_upload_service.add_full_path_to_filename("example/")

        assert self.file_upload_service.upload_path == "example/ryan_test_1.jpg"

    def test_updating_filename_successfully_changes_the_name(self):
        self.file_upload_service.update_filename(1, "test_example")

        assert self.file_upload_service.filename == "1_11111.1_test_example"
