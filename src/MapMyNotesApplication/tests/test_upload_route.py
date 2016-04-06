from MapMyNotesApplication import application, database
import pytest
import os
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from googleapiclient.http import HttpMock, HttpRequest
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
import mock
from flask.ext.testing import TestCase
from flask import Flask, request

class TestUploadRoute(TestCase):

    def create_app(self):
        app = application
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),"mock-data/authorised_credentials.json")
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()
        calendar_service = Google_Calendar_Service()
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})
        service = calendar_service.build(http_mock)
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = self.app.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)

            self.cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1
        self.google_response = {
            "items": [
                {
                    "kind": "calendar#event",
                    "etag": "\"1234567891012345\"",
                    "id": "ideventcalendaritem1",
                    "status": "confirmed",
                    "htmlLink": "https://www.google.com/calendar/event?testtest",
                    "created": "2014-09-10T14:53:25.000Z",
                    "updated": "2014-09-10T14:54:12.748Z",
                    "summary": "Test Example",
                    "creator": {
                        "email": "test@gmail.com",
                        "displayName": "Tester",
                        "self": 'true'
                    },
                    "organizer": {
                        "email": "test@gmail.com",
                        "displayName": "Test",
                        "self": 'true'
                    },
                    "start": {
                        "dateTime": "2016-12-01T01:00:00+01:00"
                    },
                    "end": {
                        "dateTime": "2016-12-01T02:30:00+01:00"
                    },
                    "transparency": "transparent",
                    "visibility": "private",
                    "iCalUID": "123456789@google.com",
                    "sequence": 0,
                    "guestsCanInviteOthers": 'false',
                    "guestsCanSeeOtherGuests": 'false',
                    "reminders": {
                        "useDefault": 'true'
                    }
                }
            ]
        }


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

    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_show_image_route(self, execute_request, authorise):
        filename = 'tests/ryan_test_1.jpg'
        upload_file = open(filename, "r")
        file_list = filename.split("/")

        file_name = file_list[1]

        resource = self.client.post("/upload", data={"file": upload_file}, follow_redirects=False)

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(self.cred_obj, auth)
        authorise.return_value = oauth_return

        execute_request.return_value = self.google_response
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
