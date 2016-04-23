import os

import mock
from MapMyNotesApplication import application, database
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User
from flask.ext.testing import LiveServerTestCase
from googleapiclient.http import HttpMock
from selenium import webdriver


class TestAcceptanceShowNote(LiveServerTestCase):
    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['secret_json_file'] = os.path.join(os.path.dirname(__file__), "mock-data/client_secret.json")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.credentials = os.path.join(os.path.dirname(__file__), "mock-data/credentials.json")
        self.authorised_credentials = os.path.join(os.path.dirname(__file__), "mock-data/authorised_credentials.json")

        self.discovery_mock = os.path.join(os.path.dirname(__file__), "mock-data/calendar-discovery.json")

        http_mock = HttpMock(self.credentials, {'status': 200})
        oauth_service = OauthService()
        file_path = app.config['secret_json_file']

        oauth_service.store_secret_file(file_path)
        flow = oauth_service.create_flow_from_clients_secret()
        self.credentials_oauth = oauth_service.exchange_code(flow, "123code", http=http_mock)

        cred_obj = oauth_service.create_credentials_from_json(self.credentials_oauth.to_json())

        auth = HttpMock(self.authorised_credentials, {'status': 200})
        self.oauth_return = oauth_service.authorise(auth, self.credentials_oauth.to_json())

        calendar_service = GoogleCalendarService()
        http_mock = HttpMock(self.discovery_mock, {'status': '200'})
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
                "summary": "CS31310",
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
                    "dateTime": "2016-12-01T01:00:00+00:00"
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
        self.new_event = {"items": [
            {
                "kind": "calendar#event",
                "etag": "\"12334455667\"",
                "id": "123456789",
                "status": "confirmed",
                "htmlLink": "http://localhost/show_note/1",
                "created": "2016-03-24T08:59:46.000Z",
                "updated": "2016-03-27T22:42:07.278Z",
                "summary": "Test To Show Hannah",
                "creator": {
                    "email": "test@gmail.com",
                    "displayName": "Test",
                    "self": True
                },
                "organizer": {
                    "email": "test@gmail.com",
                    "displayName": "test",
                    "self": True
                },
                "start": {
                    "dateTime": "2016-03-24T07:30:00Z"
                },
                "end": {
                    "dateTime": "2016-03-24T08:30:00Z"
                },
                "iCalUID": "test124@google.com",
                "sequence": 0,
                "reminders": {
                    "useDefault": True
                }
            }
        ]
        }
        self.updated_response = {
            "kind": "calendar#event",
            "etag": "\"12334455667\"",
            "id": "123456789",
            "status": "confirmed",
            "htmlLink": "http://localhost/show_note/1",
            "created": "2016-03-24T08:59:46.000Z",
            "updated": "2016-03-27T22:42:07.278Z",
            "summary": "Test To Show Hannah",
            "description": "\"http://localhost:5000/show_note/1\"",
            "creator": {
                "email": "test@gmail.com",
                "displayName": "Test",
                "self": True
            },
            "organizer": {
                "email": "test@gmail.com",
                "displayName": "test",
                "self": True
            },
            "start": {
                "dateTime": "2016-03-24T07:30:00Z"
            },
            "end": {
                "dateTime": "2016-03-24T08:30:00Z"
            },
            "iCalUID": "test124@google.com",
            "sequence": 0,
            "reminders": {
                "useDefault": True
            }
        }

        self.patch = mock.patch.object(SessionHelper, "check_if_session_contains_credentials")
        self.cred_mock = self.patch.start()
        self.cred_mock.return_value = True

        self.auth_patch = mock.patch.object(SessionHelper, "return_session_credentials")
        self.auth_mock = self.auth_patch.start()
        self.auth_mock.return_value = self.credentials_oauth.to_json()

        self.user_id = User.query.first().id

        self.user_patch = mock.patch.object(SessionHelper, 'return_user_id')
        self.user_mock = self.user_patch.start()
        self.user_mock.return_value = self.user_id

        self.user_in_session = mock.patch.object(SessionHelper,
                                                 'is_user_id_in_session')
        self.user_in_session_mock = self.user_in_session.start()
        self.user_in_session_mock.return_value = True

        self.oauth_patch = mock.patch.object(OauthService, "authorise")
        self.oauth_mock = self.oauth_patch.start()
        self.oauth_mock.return_value = self.oauth_return

        self.google_patch = mock.patch.object(GoogleCalendarService, "execute_request")
        self.google_mock = self.google_patch.start()
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        self.google_mock.side_effect = [self.google_response, self.updated_response]

        self.credentials_patch = mock.patch.object(OauthService, 'get_credentials')
        self.credentials_mock = self.credentials_patch.start()
        self.credentials_mock.return_value = oauth_service.credentials

        return app

    def setUp(self):
        # Ideas on how to create the driver and use it. https://realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640)
        database.session.close()
        database.drop_all()
        database.create_all()
        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()
        mock.patch.stopall()
        self.create_app()

    def tearDown(self):
        self.driver.quit()
        mock.patch.stopall()

    def test_image_loads_on_show_note_page(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        image_src = self.driver.find_element_by_tag_name('img').get_attribute('src')
        url_path = image_src.split("http://localhost:5000")

        assert url_path[1] == "/img/test.png"

    def test_module_code_is_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        module_code = self.driver.find_element_by_class_name("module_code")

        assert module_code.text == "Module Code: CS31310"

    def test_lecturer_name_is_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")

        assert lecturer_name.text == "By Mr Foo"

    def test_location_name_is_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        location_name = self.driver.find_element_by_class_name("location_name")

        assert location_name.text == "C11 Hugh Owen"

    def test_date_values_are_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        date_value = self.driver.find_element_by_class_name("date")

        assert date_value.text == "12 February 2016 16:00"

    def test_title_value_are_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        title = self.driver.find_element_by_class_name("title")

        assert title.text == "Title"

    def test_delete_link_is_available(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        delete_link = self.driver.find_element_by_class_name('delete_note')

        delete_form = self.driver.find_element_by_class_name('delete_note_form').get_attribute("action").split(
            "http://localhost:5000")

        assert delete_link.is_displayed() is True

        assert delete_form[1] == "/delete_note/1"

    def test_edit_link_is_available(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12 February 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        edit_form = self.driver.find_element_by_class_name("edit_note_form").get_attribute("action").split(
            "http://localhost:5000")

        edit_link = self.driver.find_element_by_class_name('edit_note')

        assert edit_link.is_displayed() is True

        assert edit_form[1] == "/metadata/edit/1"

    def test_displaying_whether_event_was_added_a_users_calendar_return_true(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("1 December 2016")
        time = self.driver.find_element_by_class_name("time")
        time.send_keys("01:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        saved_to_cal = self.driver.find_element_by_class_name("saved_to_cal")

        calendar_link = self.driver.find_element_by_class_name('calendar_link').get_attribute("href")

        assert "Successfully saved to calendar" in saved_to_cal.text
        assert "http://localhost/show_note/1" in calendar_link
