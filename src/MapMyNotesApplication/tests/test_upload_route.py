from MapMyNotesApplication import application
import pytest
import os


class TestUploadRoute(object):

    def setup(self):
        self.app = application.test_client()

    def teardown(self):
        if os.path.isfile("MapMyNotesApplication/upload/ryan_test_1.jpg"):
            os.remove("MapMyNotesApplication/upload/ryan_test_1.jpg")

    def test_get_upload_route(self):
        resource = self.app.get("/upload")
        assert resource.status_code is 200

    def test_put_upload_route(self):
        resource = self.app.put("/upload")
        assert resource.status_code is not 200

    def test_uploading_file_status(self):
        # Adapted from http://stackoverflow.com/questions/20080123/testing-file-upload-with-flask-and-python-3
        upload_file = open("tests/ryan_test_1.jpg", "r")
        resource = self.app.post("/upload", data={"file": upload_file})

        assert "bad file" is not resource.data

        assert resource.status_code is 200

    def test_uploading_without_file_attached(self):
        resource = self.app.post("/upload", data={})

        assert resource.status_code is not 200

    def test_saving_file_attached(self):
        upload_file = open("tests/ryan_test_1.jpg", "r")

        resource = self.app.post("/upload", data={"file": upload_file})

        assert resource.status_code is 200

        assert True is os.path.isfile("MapMyNotesApplication/upload/ryan_test_1.jpg")
