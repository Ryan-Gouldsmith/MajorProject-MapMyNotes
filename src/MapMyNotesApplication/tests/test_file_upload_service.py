from MapMyNotesApplication import application
import pytest
import os
from MapMyNotesApplication.models.file_upload_service import FileUploadService
from werkzeug.datastructures import FileStorage

class TestFileUploadService(object):

    def setup(self):
        self.app = application.test_client()
        self.file_upload_service = FileUploadService()
        self.file_test_upload_path = "MapMyNotesApplication/upload/ryan_test_1.jpg"

    def teardown(self):
        if os.path.isfile(self.file_test_upload_path):
            os.remove(self.file_test_upload_path)

    def test_file_upload_with_slash(self):
        filename = "test_directory/file.jpg"
        expected = self.file_upload_service.is_forward_slash_in_filename(filename)

        assert expected is True

    def test_file_upload_without_slash(self):
        filename = "file.jpg"
        expected = self.file_upload_service.is_forward_slash_in_filename(filename)

        assert expected is False

    def test_prepare_file_path_file(self):
        filename = "test_directory/file.jpg"

        prepared_filename = self.file_upload_service.prepare_file_path_file(filename)

        expected = "file.jpg"

        assert prepared_filename == expected

    def test_prepare_file_path_file_check_slash(self):
        filename = "test_directory/file.jpg"

        prepared_filename = self.file_upload_service.prepare_file_path_file(filename)

        assert "/" not in prepared_filename

    def test_saving_a_filaname_to_uploads(self):
        upload_directory = "MapMyNotesApplication/upload/"
        filename = "tests/ryan_test_1.jpg"
        file_object = open(filename, 'r')
        # Found out I can use the File Storage object to mock the File used in the controller for Flask http://stackoverflow.com/questions/18249949/python-file-object-to-flasks-filestorage
        file = FileStorage(file_object)

        prepared_filename = self.file_upload_service.prepare_file_path_file(file.filename)

        print prepared_filename

        expected_file = upload_directory + prepared_filename

        self.file_upload_service.save_users_file(prepared_filename, file)

        assert os.path.isfile(expected_file) is True