from MapMyNotesApplication import application, database
import pytest
import os
from MapMyNotesApplication.models.note import Note
from flask.ext.testing import TestCase
from flask import Flask, request

class TestUploadRoute(TestCase):

    def create_app(self):
        app = application
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

    def tearDown(self):
        if os.path.isfile("MapMyNotesApplication/upload/ryan_test_1.jpg"):
            os.remove("MapMyNotesApplication/upload/ryan_test_1.jpg")

        if os.path.isfile('MapMyNotesApplication/upload/ryan_test_1.tif'):
            os.remove('MapMyNotesApplication/upload/ryan_test_1.tif')

    def test_get_upload_route(self):
        resource = self.client.get("/upload")
        assert resource.status_code is 200

    def test_put_upload_route(self):
        resource = self.client.put("/upload")
        assert resource.status_code is not 200

    def test_uploading_file_status(self):
        # Adapted from http://stackoverflow.com/questions/20080123/testing-file-upload-with-flask-and-python-3
        upload_file = open("tests/ryan_test_1.jpg", "r")
        resource = self.client.post("/upload", data={"file": upload_file}, follow_redirects = False)

        assert "bad file" is not resource.data

        assert resource.status_code == 302

    def test_uploading_without_file_attached(self):
        resource = self.client.post("/upload", data={}, follow_redirects = False)

        assert resource.status_code is not 200

    def test_saving_file_attached(self):
        upload_file = open("tests/ryan_test_1.jpg", "r")

        resource = self.client.post("/upload", data={"file": upload_file})

        assert resource.status_code == 302

        assert True is os.path.isfile("MapMyNotesApplication/upload/ryan_test_1.jpg")

    def test_uploading_right_file_extension(self):
        upload_file = open("tests/ryan_test_1.jpg", "r")

        resource = self.client.post("/upload", data={"file": upload_file})

        assert resource.status_code == 302

        assert "Error: Wrong file extention in uploaded file" not in resource.data

    def test_uploading_wrong_file_extension(self):
        upload_file = open("tests/ryan_test_1.pdf", "r")

        resource = self.client.post("/upload", data={"file": upload_file}, follow_redirects = False)

        assert resource.status_code is 200

        assert "Error: Wrong file extention in uploaded file"  in resource.data

    def test_show_image_route(self):
        filename = 'tests/ryan_test_1.jpg'
        upload_file = open(filename, "r")
        file_list = filename.split("/")

        file_name = file_list[1]

        resource = self.client.post("/upload", data={"file": upload_file}, follow_redirects=False)

        resource = self.client.get("/upload/show_image/" + file_name, follow_redirects=False)

        assert resource.status_code is 200

    def test_should_not_allow_post_to_show_image_route(self):
        file_list = 'tests/ryan_test_1.jpg'.split("/")

        file_name = file_list[1]

        resource = self.client.post("/upload/show_image/" + file_name)

        assert resource.status_code is not 200

    def test_when_uploaded_file_redirects_to_show_image_route(self):
        upload_file = open("tests/ryan_test_1.jpg", "r")

        resource = self.client.post("/upload", data={"file": upload_file}, follow_redirects = False)

        # Used their idea how to get the location as there was nothing in the documents to say. Modified it for my own splitting. http://stackoverflow.com/questions/22566627/flask-unit-testing-getting-the-responses-redirect-location
        url_full = resource.headers.get("Location")

        url_path = url_full.split("http://localhost")

        expected_url = "/upload/show_image/ryan_test_1.jpg"
        # checks the last part after the localhost.
        assert url_path[1] == expected_url

    def test_should_return_200_error_on_404_page(self):
        resource = self.client.get("/error/404")

        assert resource.status_code is 200

    def test_should_return_image(self):
        upload_file = open("tests/ryan_test_1.jpg", "r")

        resource = self.client.post("/upload", data={"file": upload_file}, follow_redirects = False)

        resource = self.client.get('/img/ryan_test_1.jpg')

        assert resource.headers.get("Content-Type") == "image/jpeg"
        assert resource.status_code == 200

    def test_should_save_the_correct_tif_file_to_upload(self):
        upload_file = open("tests/ryan_test_1.jpg", "r")
        resource = self.client.post("/upload", data={"file": upload_file}, follow_redirects = False)

        assert os.path.isfile("MapMyNotesApplication/upload/ryan_test_1.tif") is True
