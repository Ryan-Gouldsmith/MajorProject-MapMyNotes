from MapMyNotesApplication import application
import pytest
import os
from MapMyNotesApplication.models.file_upload_service import FileUploadService

class TestFileUploadService(object):

    def setup(self):
        self.app = application.test_client()
        self.file_upload_service = FileUploadService()

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

    
