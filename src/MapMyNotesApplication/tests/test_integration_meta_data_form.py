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
from MapMyNotesApplication.models.tesseract_helper import TesseractHelper
import os


"""https://books.google.co.uk/books?id=Xd0DCgAAQBAJ&pg=PA77&lpg=PA77&dq=flask-testing+liveservertestcase+selenium&source=bl&ots=fhCVat8wgm&sig=2ehfPK93v8fS2NQEq_vzdKYbc-U&hl=en&sa=X&ved=0ahUKEwiCr7ns6KLLAhVCUhQKHVO0DWoQ6AEIPTAF#v=onepage&q=flask-testing%20liveservertestcase%20selenium&f=false Docs are terrible this book may be good. http://www.voidspace.org.uk/python/mock/patch.html#patch-methods-start-and-stop This is great. Helped with the mocking and found it really useful part of the library. It meant that all the other tests passed and I could mock the functions for the acceptance tests.
http://makina-corpus.com/blog/metier/2013/dry-up-mock-instanciation-with-addcleanup Was also a good reference for the testing with the mocks. I learnt a lot from this resource
"""
class TestIntegrationMetaDataForm(LiveServerTestCase):

    def create_app(self):
        print "creating app"

        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'Secret_pass_phrase'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__),"mock-data/authorised_credentials.json")

        http_mock = HttpMock(self.credentials, {'status': 200})
        oauth_service = Oauth_Service()
        file_path = app.config['secret_json_file']

        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()
        self.credentials_oauth = oauth_service.exchange_code(flow, "123code",
                    http=http_mock)

        cred_obj = oauth_service.create_credentials_from_json(self.credentials_oauth.to_json())

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        self.oauth_return = oauth_service.authorise(cred_obj, auth)

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")
        calendar_service = Google_Calendar_Service()

        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})
        service = calendar_service.build(http_mock)

        self.google_response = {"items": [
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
           "dateTime": "2016-12-01T01:00:00Z"
          },
          "end": {
           "dateTime": "2016-12-01T02:30:00Z"
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
        #self.old_session = SessionHelper.check_if_session_contains_credentials
        #SessionHelper.check_if_session_contains_credentials = mock.Mock(return_value=True)
        #self.old_cred = SessionHelper.return_session_credentials
        #SessionHelper.return_session_credentials = mock.Mock(return_value = self.credentials_oauth.to_json())

        #Oauth_Service.authorise = mock.Mock(return_value = self.oauth_return )
        self.patch = mock.patch.object(SessionHelper, "check_if_session_contains_credentials")
        self.cred_mock = self.patch.start()
        self.cred_mock.return_value = True

        self.auth_patch = mock.patch.object(SessionHelper, "return_session_credentials")
        self.auth_mock = self.auth_patch.start()
        self.auth_mock.return_value = self.credentials_oauth.to_json()

        self.oauth_patch = mock.patch.object(Oauth_Service, "authorise")
        self.oauth_mock = self.oauth_patch.start()
        self.oauth_mock.return_value = self.oauth_return

        self.google_patch = mock.patch.object(Google_Calendar_Service, "execute_request")
        self.google_mock = self.google_patch.start()
        self.google_mock.return_value = self.google_response

        self.tesseract_patch = mock.patch.object(TesseractHelper, 'get_confidence_and_words_from_image')
        self.user_mock = self.tesseract_patch.start()
        self.user_mock.return_value = [[(u'CS4192250:', 75), (u'A', 88), (u't-.tLe.', 72), (u'.9oes', 72), (u'here\n\n', 81)], [(u'Date:', 73), (u'29', 93), (u'/3/2016', 83), (u'15..', 76), (u'e0\n\n', 63)], [(u'By:', 69), (u'A', 89), (u'c".crlain', 65), (u'doc.tor', 74), (u'tiHe\n\n', 75)]]

        return app

    def setUp(self):
        self.create_app()
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )

    def tearDown(self):
        print "deleting"
        self.driver.quit()
        mock.patch.stopall()

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
        assert suggested_date.text == '2016-01-31 13:47:14'

    def test_form_does_not_show_exif_data_if_image_is_a_png(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        suggested_date = self.driver.find_element_by_class_name('suggested_date')
        assert suggested_date.text == 'No suitable date was found from the note'


    def test_google_calendar_event_shows_when_exif_data_matches(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test2.jpg")
        calendar_date =  self.driver.find_element_by_class_name("suggested_calendar_event")
        assert calendar_date.is_displayed() is True

        calendar_event_title = self.driver.find_element_by_class_name("calendar_event_title")
        calendar_event_date = self.driver.find_element_by_class_name("calendar_start_time")
        view_event = self.driver.find_element_by_class_name("calendar_event_view")

        assert "Test Example" in calendar_event_title.text
        assert "01 December 2016 01:00" in calendar_event_date.text
        assert "View event" in view_event.text

    def test_tesseract_data_shows_when_image_is_uploaded(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name("tesseract_module_code")
        lecture_title = self.driver.find_element_by_class_name('tesseract_title')
        date = self.driver.find_element_by_class_name("tesseract_date")
        lecturer = self.driver.find_element_by_class_name("tesseract_lecturer")

        assert module_code.text == "CS4192250:"
        assert lecture_title.text == 'A t-.tLe. .9oes here'
        assert date.text == "Date: 29 /3/2016 15.. e0"
        assert lecturer.text == 'By: A c".crlain doc.tor tiHe'

    def test_tesseract_data_is_coloured_correctly_for_confidence(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        #http://www.hexcolortool.com/ hex to rgba converter
        green = "rgba(76, 175, 80, 1)"

        orange = "rgba(255, 152, 0, 1)"

        red = "rgba(244, 67, 54, 1)"
        module_code = self.driver.find_element_by_css_selector("p.tesseract_module_code span")
        lecture_title = self.driver.find_elements_by_css_selector('p.tesseract_title span')
        date = self.driver.find_elements_by_css_selector("p.tesseract_date span")
        lecturer = self.driver.find_element_by_class_name("tesseract_lecturer")
        print self.driver.page_source
        assert module_code.value_of_css_property("color") == green

        assert lecture_title[0].value_of_css_property("color") == green
        assert lecture_title[1].value_of_css_property("color") == orange
        assert lecture_title[2].value_of_css_property("color") == orange
        assert lecture_title[3].value_of_css_property("color") == green

        assert date[0].value_of_css_property("color") == orange
        assert date[1].value_of_css_property("color") == green
        assert date[2].value_of_css_property("color") == green
        assert date[3].value_of_css_property("color") == green
