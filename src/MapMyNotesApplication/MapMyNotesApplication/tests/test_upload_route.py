from MapMyNotesApplication.MapMyNotesApplication import application
import pytest
import os


class TestUploadRoute(object):

    def setup(self):
        self.app = application.test_client()

    def test_get_upload_route(self):
        resource = self.app.get("/upload")
        assert resource.status_code == 200

    def test_put_upload_route(self):
        resource = self.app.put("/upload")
        assert resource.status_code is not 200

    def test_uploading_file_status(self):
        upload_file = open("tests/ryan_test_1.jpg", "r")
        resource = self.app.post("/upload", data={"file": upload_file})

        assert "bad file" is not resource.data

        assert resource.status_code is 200

    def test_uploading_without_file_attached(self):
        resource = self.app.post("/upload", data={})

        assert resource.status_code is not 200
