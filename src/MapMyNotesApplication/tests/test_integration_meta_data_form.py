from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask, session, current_app
from flask.ext.testing import LiveServerTestCase
import mock
from MapMyNotesApplication.models.file_upload_service import FileUploadService
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from googleapiclient.http import HttpMock, HttpRequest
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.session_helper import SessionHelper
import os


#https://books.google.co.uk/books?id=Xd0DCgAAQBAJ&pg=PA77&lpg=PA77&dq=flask-testing+liveservertestcase+selenium&source=bl&ots=fhCVat8wgm&sig=2ehfPK93v8fS2NQEq_vzdKYbc-U&hl=en&sa=X&ved=0ahUKEwiCr7ns6KLLAhVCUhQKHVO0DWoQ6AEIPTAF#v=onepage&q=flask-testing%20liveservertestcase%20selenium&f=false Docs are terrible this book may be good.
class TestIntegrationMetaDataForm(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'sekrit!'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        #app = application
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),"mock-data/authorised_credentials.json")
        http_mock = HttpMock(self.credentials, {'status': 200})
        oauth_service = Oauth_Service()
        file_path = application.config['secret_json_file']

        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()
        credentials = oauth_service.exchange_code(flow, "123code",
                    http=http_mock)

        cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

        SessionHelper.check_if_session_contains_credentials = mock.Mock(return_value = True)

        SessionHelper.return_session_credentials = mock.Mock(return_value = credentials.to_json())


        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = oauth_service.authorise(cred_obj, auth)
        Oauth_Service.authorise = mock.Mock(return_value=oauth_return)

        Google_Calendar_Service.execute_request = mock.Mock(return_value={"items": [
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
        })
        return app

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )

    def tearDown(self):
        self.driver.quit()


    def test_form_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        form = self.driver.find_element_by_tag_name('form')
        assert form.is_displayed() is True

    def test_submit_button_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        submit_button = self.driver.find_element_by_class_name("submit")
        assert submit_button.is_displayed() is True

    def test_module_field_label_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        module_label = self.driver.find_element_by_class_name("module_label")
        assert module_label.is_displayed() is True

    def test_module_field_label_content(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        module_label_content = self.driver.find_element_by_class_name("module_label")
        assert module_label_content.text == "Module Code:"

    def test_form_has_module_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        module_field = self.driver.find_element_by_class_name("module_code_data")
        assert module_field.is_displayed() is True

    def test_form_has_correct_url_action(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        form_action = self.driver.find_element_by_tag_name("form").get_attribute("action")

        path = form_action.split("http://localhost:5000")

        expected_url = "/metadata/add/test2.jpg"
        assert expected_url == path[1]

    def test_form_has_lecturer_name_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        lecturer_field = self.driver.find_element_by_class_name("lecturer_name")
        assert lecturer_field.is_displayed() is True

    def test_form_has_location_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        location_field = self.driver.find_element_by_class_name("location_name")

        assert location_field.is_displayed() is True

    def test_form_has_date_of_lecturer_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        date_field = self.driver.find_element_by_class_name("date")

        assert date_field.is_displayed() is True

    def test_form_has_title_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        title_field = self.driver.find_element_by_class_name('title')
        assert title_field.is_displayed() is True

    def test_form_shows_exif_data_from_image(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        suggested_date = self.driver.find_element_by_class_name('suggested_date')
        assert suggested_date.text == '2016:01:31 13:47:14'

    def test_form_does_not_show_exif_data_if_image_is_a_png(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        suggested_date = self.driver.find_element_by_class_name('suggested_date')
        assert suggested_date.text == 'No suitable date was found from the note'

    def test_google_calendar_event_shows_when_exif_data_matches(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        calendar_date = self.driver.find_element_by_class_name("suggested_calendar_event")
        assert calendar_date.is_displayed() is True
        calendar_event_title = self.driver.find_element_by_class_name("calendar_event_title")
        calendar_event_date = self.driver.find_element_by_class_name("calendar_start_time")
        view_event = self.driver.find_element_by_class_name("calendar_event_view")

        assert "Test Example" in calendar_event_title.text
        assert "01 December 2016 01:00:00" in calendar_event_date.text
        assert "View event" in view_event.text
