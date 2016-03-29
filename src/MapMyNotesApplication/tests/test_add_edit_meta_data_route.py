from MapMyNotesApplication import application, database
import pytest
import os
import mock
from googleapiclient.http import HttpMock, HttpRequest
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from datetime import datetime
from flask import Flask
from flask.ext.testing import TestCase


class TestAddEditMetaDataRoute(TestCase):

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
        file_list = 'tests/test.png'.split("/")

        test_image_2 = "tests/test.png".split("/")

        self.image = file_list[1]
        self.second_image = test_image_2[1]

        calendar_service = Google_Calendar_Service()
        http_mock = HttpMock(self.discovery_mock, {'status' : '200'})
        service = calendar_service.build(http_mock)

        database.session.close()
        database.drop_all()
        database.create_all()

    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_add_meta_data_route_returns_302(self, execute_request, authorise):
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = application.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)
            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1


        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(cred_obj, auth)
        authorise.return_value = oauth_return

        authorise.return_value = oauth_return
        Google_Calendar_Service.execute_request.return_value = {"items": [
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

        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}

        resource = self.client.post('/metadata/add/' + self.image,       content_type='multipart/form-data', data=post_data, follow_redirects=False)

        assert resource.status_code == 302

    def test_add_meta_data_route_get_request_not_allowed(self):
        resource = self.client.get('/metadata/add/' + self.image)
        assert resource.status_code == 405

    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_add_module_code_via_post_request_successfully(self, authorise, execute_request):
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = self.app.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)

            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(cred_obj, auth)
        authorise.return_value = oauth_return

        execute_request.return_value = {"items": [
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
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
            content_type='multipart/form-data',
            data=post_data, follow_redirects=False)

        assert len(Module_Code.query.all()) == 1

    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_it_saves_a_note_object_once_the_meta_data_added(self, execute_request, authorise):
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = self.app.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)

            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(cred_obj, auth)
        authorise.return_value = oauth_return

        execute_request.return_value = {"items": [
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
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
            content_type='multipart/form-data',
            data=post_data, follow_redirects=False)

        note = Note.query.first()
        assert note.image_path == "test.png"
        assert note.meta_data.module_code.module_code == "CS31310"
        assert note.meta_data.lecturer == "Mr Foo"
        assert note.meta_data.location == "C11 Hugh Owen"

    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_once_a_note_is_saved_it_redirects_to_show_note(self, execute_request, authorise):
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = self.app.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)

            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(cred_obj, auth)
        authorise.return_value = oauth_return

        execute_request.return_value = {"items": [
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
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)

        url_redirect = resource.headers.get("Location")
        url_path = url_redirect.split("http://localhost")

        expected_url = "/show_note/1"
        # checks the last part after the localhost.
        assert expected_url in url_path[1]

    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_using_the_same_module_code_as_before_if_one_exists(self, execute_request, authorise):
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = self.app.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)

            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(cred_obj, auth)
        authorise.return_value = oauth_return

        execute_request.return_value = {"items": [
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
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)

        second_resource = self.client.post("/metadata/add/" + self.second_image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)


        notes = Note.query.all()

        note_one = notes[0]

        note_two = notes[1]

        expected_module_code_id = note_one.meta_data.module_code.id

        assert expected_module_code_id == note_two.meta_data.module_code.id

    @mock.patch.object(Oauth_Service, 'authorise')
    @mock.patch.object(Google_Calendar_Service, 'execute_request')
    def test_using_the_different_module_code_should_save_new_code(self, execute_request, authorise):
        #http://stackoverflow.com/questions/28908167/cant-upload-file-and-data-in-same-request-in-flask-test Got the content-type idea for the form here
        with self.client.session_transaction() as session:
            http_mock = HttpMock(self.credentials, {'status': 200})
            oauth_service = Oauth_Service()
            file_path = self.app.config['secret_json_file']

            oauth_service.store_secret_file(file_path)
            flow = oauth_service.create_flow_from_clients_secret()
            credentials = oauth_service.exchange_code(flow, "123code",
            http=http_mock)

            cred_obj = oauth_service.create_credentials_from_json(credentials.to_json())

            session['credentials'] = credentials.to_json()
            session['user_id'] = 1

        auth = HttpMock(self.authorised_credentials, {'status' : 200})
        oauth_return = Oauth_Service.authorise(cred_obj, auth)
        authorise.return_value = oauth_return

        execute_request.return_value = {"items": [
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
        post_data = {"module_code_data":"CS31310", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        resource = self.client.post("/metadata/add/" + self.image,
                content_type='multipart/form-data',
                data=post_data, follow_redirects=False)

        post_data_second = {"module_code_data":"SE315120", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}
        second_resource = self.client.post("/metadata/add/" + self.second_image,
                content_type='multipart/form-data',
                data=post_data_second, follow_redirects=False)

        notes = Note.query.all()

        note_one = notes[0]

        note_two = notes[1]

        actual = note_one.meta_data.module_code.id

        expected = note_two.meta_data.module_code.id

        assert actual != expected

    def test_get_edit_note_information_returns_200_success(self):

        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "A Title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        resource = self.client.get("/metadata/edit/" + str(note.id), follow_redirects=False)

        assert resource.status_code == 200

    def test_post_to_edit_note_different_data_created_new_meta_data(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()

        meta_data_change = {"module_code_data":"SE315120", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note.id), content_type='multipart/form-data',
        data=meta_data_change, follow_redirects=False)


        note_meta_data = Note_Meta_Data.query.all()
        assert len(note_meta_data) is 2

    def test_post_to_edit_note_changes_the_foreign_key_association(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id

        meta_data_change = {"module_code_data":"SE315120", "lecturer_name_data" : "Mr Foo", 'location_data': "C11 Hugh Owen", "date_data": "12 February 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note.id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        note_found = Note.query.get(note_id)
        assert note_found.note_meta_data_id is 2

    def test_post_with_already_existing_meta_data_should_return_instance(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id


        module_code_two = Module_Code('CS361010')
        database.session.add(module_code_two)
        database.session.commit()
        module_code_id = module_code_two.id

        date = datetime.strptime("24 January 2016 16:00", "%d %B %Y %H:%M")

        changed_meta_data= Note_Meta_Data("Changed Text", module_code_id, 'Test room', date, "Another note title")
        changed_meta_data.save()
        changed_meta_data_id = changed_meta_data.id

        meta_data_change = {"module_code_data":"CS361010", "lecturer_name_data" : "Changed Text", 'location_data': "Test room", "date_data": "24 January 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note_id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        note_found = Note.query.get(note_id)

        assert note_found.meta_data.id == changed_meta_data_id

    def test_posting_exisiting_module_code_new_meta_data_new_instance(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, 'Another note title')
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id

        meta_data_change = {"module_code_data":"CS31310", "lecturer_name_data" : "Changed Text", 'location_data': "Test room", "date_data": "24 January 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note_id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        note_found = Note.query.get(note_id)

        assert note_found.meta_data.id is 2

    def test_posting_redirects_back_to_show_note(self):
        file_path = "upload/test.png"
        module_code = Module_Code('CS31310')
        database.session.add(module_code)
        database.session.commit()

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = Note_Meta_Data("Mr Foo", module_code.id, 'C11 Hugh Owen', date, "Note title")
        note_meta_data.save()

        note = Note(file_path,note_meta_data.id)
        note.save()
        note_id = note.id

        meta_data_change = {"module_code_data":"CS31310", "lecturer_name_data" : "Changed Text", 'location_data': "Test room", "date_data": "24 January 2016 16:00", "title_data": "A Title"}

        response = self.client.post("/metadata/edit/" + str(note_id), content_type='multipart/form-data',data=meta_data_change, follow_redirects=False)

        assert response.status_code == 302
        location = response.headers.get("Location").split("http://localhost/")
        assert location[1] == "show_note/1"
