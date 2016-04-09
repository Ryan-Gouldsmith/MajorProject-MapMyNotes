import os
from datetime import datetime

import httplib2
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User
from dateutil import tz
from flask import Blueprint, render_template, request, url_for, redirect, session

metadata = Blueprint('metadata', __name__)

POST = "POST"
GET = "GET"


@metadata.route("/metadata/add/<note_image>", methods=[POST])
def add_meta_data(note_image):
    session_helper = SessionHelper(session)
    if session_helper.is_user_id_in_session() is False:
        return redirect(url_for('homepage.home_page_route'))

    service = OauthService()
    session_credentials = session_helper.return_session_credentials()
    http_auth = service.authorise(httplib2.Http(), session_credentials)
    credentials = service.get_credentials()

    if credentials.access_token_expired:
        return redirect(url_for('logout.logout'))

    if request.method == POST:

        if check_all_params_exist(request.form) is False:
            error = "Some fields are missing"
            session_helper.set_errors_in_session(error)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        if date_formatted_correctly(request.form['date_data']) is False:
            error = "Wrong date format: should be date month year hour:minute, eg: 20 February 2016"
            session_helper.set_errors_in_session(error)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        if time_formatted_correctly(request.form['time_data']) is False:
            error = "Wrong time format: should be hour:minute, e.g 13:00"
            session_helper.set_errors_in_session(error)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        any_errors, errors = check_all_params_are_less_than_schema_length(request.form)
        if any_errors is True:
            session_helper.set_errors_in_session(errors)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        module_code_data = request.form['module_code_data'].upper()
        lecturer_name_data = request.form['lecturer_name_data']
        location_data = request.form['location_data']
        date_data = request.form['date_data']
        time_data = request.form['time_data']
        title_data = request.form['title_data']

        file_path = "MapMyNotesApplication/upload/" + note_image

        if module_code_data and os.path.isfile(file_path):
            module_code_obj = ModuleCode.find_id_by_module_code(module_code_data)
            if module_code_obj is None:
                module_code_obj = ModuleCode(module_code_data)
                module_code_obj.save()

            module_code_id = module_code_obj.id
            date_time = convert_string_date_and_time_to_datetime(date_data, time_data)
            note_meta_data = NoteMetaData(lecturer_name_data, module_code_id, location_data, date_time, title_data)
            note_meta_data.save()

            user_id = session_helper.return_user_id()
            user = User.query.get(user_id)
            note = Note(note_image, note_meta_data.id, user.id)
            note.save()

            google_calendar_service = GoogleCalendarService()
            note_url = google_calendar_service.prepare_url_for_event(note)
            google_service = google_calendar_service.build(http_auth)

            start_date, end_date = process_time_zone(date_time)
            google_request = google_calendar_service.get_list_of_events(google_service, start=start_date, end=end_date)

            google_calendar_response = google_calendar_service.execute_request(google_request, http_auth)
            module_code = module_code_obj.module_code

            event = get_event_containing_module_code(module_code, google_calendar_response, date_time)

            saved_response = None
            if event is not None:
                saved_response = add_url_to_event(google_calendar_service, google_service, note_url, event, http_auth)

            if saved_response is not None and note_url in saved_response['description']:
                note.update_calendar_url(saved_response['htmlLink'])

            return redirect(url_for('shownote.show_note', note_id=note.id))
    return redirect(url_for('fileupload.error_four_zero_four'))


@metadata.route("/metadata/edit/<note_id>", methods=[GET, POST])
def edit_meta_data(note_id):
    session_helper = SessionHelper(session)
    service = OauthService()
    session_credentials = session_helper.return_session_credentials()
    http_auth = service.authorise(httplib2.Http(), session_credentials)
    credentials = service.get_credentials()

    if credentials.access_token_expired:
        return redirect(url_for('logout.logout'))

    if request.method == GET:
        errors = None
        if session_helper.errors_in_session():
            errors = session_helper.get_errors()
            session_helper.delete_session_errors()

        note = Note.query.get(note_id)
        module_code = note.meta_data.module_code.module_code
        lecturer = note.meta_data.lecturer
        location = note.meta_data.location
        date = note.meta_data.date.strftime("%d %B %Y")
        time = note.meta_data.date.strftime("%H:%M")
        title = note.meta_data.title

        return render_template('/file_upload/edit_meta_data.html', module_code=module_code, lecturer=lecturer,
                               location=location, date=date, time=time, title=title, note_image=note.image_path,
                               errors=errors)

    elif request.method == POST:
        # Get the note NO TESTS FOR THIS
        note = Note.query.get(note_id)
        # Call the calendar event for the given date of a note
        previous_date = note.meta_data.date
        start_date, end_date = process_time_zone(previous_date)

        google_calendar_service = GoogleCalendarService()
        note_url = google_calendar_service.prepare_url_for_event(note)
        google_service = google_calendar_service.build(http_auth)

        google_request = google_calendar_service.get_list_of_events(google_service, start=start_date, end=end_date)

        google_calendar_response = google_calendar_service.execute_request(google_request, http_auth)
        module_code = note.meta_data.module_code.module_code

        # Check to see if the description contains the string of the note
        event = get_event_containing_module_code(module_code, google_calendar_response, previous_date)
        if event and 'description' in note_url and note_url in event['description']:
            # Remove the string from the description
            response = add_url_to_event(google_calendar_service, google_service, "", event, http_auth)
            # TODO check the response is empty

        if check_all_params_exist(request.form) is False:
            session['errors'] = "Some fields are missing"
            return redirect(url_for('metadata.edit_meta_data', note_id=note_id))

        if date_formatted_correctly(request.form['date_data']) is False:
            session['errors'] = "Wrong date format: should be date month year eg: 20 February 2016"
            return redirect(url_for('metadata.edit_meta_data', note_id=note_id))

        if time_formatted_correctly(request.form['time_data']) is False:
            error = "Wrong time format: should be hour:minute, e.g 13:00"
            session_helper.set_errors_in_session(error)
            return redirect(url_for('metadata.edit_meta_data', note_id=note_id))

        any_errors, errors = check_all_params_are_less_than_schema_length(request.form)
        note_image = note.image_path
        if any_errors is True:
            session['errors'] = errors
            return redirect(url_for('metadata.edit_meta_data', note_image=note_image))

        module_code_data = request.form['module_code_data'].upper()
        lecturer_name = request.form['lecturer_name_data']
        location = request.form['location_data']
        date_data = request.form['date_data']
        time_data = request.form['time_data']
        title = request.form['title_data']
        module_code = ModuleCode.find_id_by_module_code(module_code_data)
        date_time = convert_string_date_and_time_to_datetime(date_data, time_data)

        if module_code is not None:
            meta_data = NoteMetaData(lecturer_name, module_code.id, location, date_time, title)

            found_meta_data = NoteMetaData.find_meta_data(meta_data)

            note = Note.query.get(note_id)
            if found_meta_data is not None:
                note.update_meta_data_id(found_meta_data.id)
            else:
                meta_data.save()
                note.update_meta_data_id(meta_data.id)
        else:
            module_code_obj = ModuleCode(module_code_data)
            module_code_obj.save()
            module_code = module_code_obj

            note_meta_data = NoteMetaData(lecturer_name, module_code_obj.id, location, date_time, title)
            response = note_meta_data.save()
            # TODO Handle response

            note = Note.query.get(note_id)
            note.update_meta_data_id(note_meta_data.id)

        start_date, end_date = process_time_zone(previous_date)
        google_request = google_calendar_service.get_list_of_events(google_service, start=start_date, end=end_date)
        google_calendar_response = google_calendar_service.execute_request(google_request, http_auth)
        event = get_event_containing_module_code(module_code.module_code, google_calendar_response, date_time)
        note_url = google_calendar_service.prepare_url_for_event(note)
        if event:
            # Remove the string from the description
            response = add_url_to_event(google_calendar_service, google_service, note_url, event, http_auth)
            if response is not None and note_url in response['description']:
                note.update_calendar_url(response['htmlLink'])

        return redirect(url_for('shownote.show_note', note_id=note_id))


# TODO: Move the below functions to a helper class?

def check_all_params_exist(params):

    if params["module_code_data"] is None or params['lecturer_name_data'] \
            is None or params['location_data'] is None or \
            params['date_data'] is None or params['title_data'] is None or params['time_data'] is None:
        return False

    """ REFERENCE isspace checks for empty spaces
        http://stackoverflow.com/questions/2405292/how-to-check-if-text-is-empty-spaces-tabs-newlines-in-python
    """

    if params['module_code_data'].isspace() or params['lecturer_name_data'].isspace() \
            or params['location_data'].isspace() or params['date_data'].isspace() or params['title_data'].isspace() \
            or params['time_data'].isspace():
        return False

    return True


def check_all_params_are_less_than_schema_length(params):
    errors = []
    if len(params["module_code_data"]) > 50:
        errors.append("Module code length too long, max 50 characters.")

    if len(params['lecturer_name_data']) > 100:
        errors.append("Lecture name is too long, max length 100 characters")

    if len(params['location_data']) > 100:
        errors.append("Location data too long, max length 100 characters")

    if len(params['title_data']) > 100:
        errors.append("title data too long, max length 100 characters")

    return len(errors) > 0, errors


def convert_string_date_and_time_to_datetime(date, time):
    date = datetime.strptime(date, "%d %B %Y")
    time = datetime.strptime(time, "%H:%M")
    date_time = datetime.combine(date.date(), time.time())
    return date_time


def process_time_zone(date_time):
    """ Great API
    https://docs.python.org/2/library/datetime.html#datetime.datetime.replace
    Had issue with the BST. Had to supply the timezone offset to Google API.
    """
    date_time = date_time.replace(tzinfo=tz.gettz('Europe/London'))
    start_date = date_time.isoformat("T")
    end_time = datetime.strptime('23:59', "%H:%M").time()
    end_date = datetime.combine(date_time.date(), end_time)
    end_date = end_date.replace(tzinfo=tz.gettz('Europe/London'))
    end_date = end_date.isoformat("T")
    return start_date, end_date


def get_event_containing_module_code(module_code, calendar_response, start_date):
    # some events come back like 2016-02-16T10:30:00Z other's come back like 2016-02-16T10:30:00+00:00
    start_date = start_date.replace(tzinfo=None).isoformat("T")
    for event in calendar_response["items"]:
        if module_code in event['summary'].upper() and start_date in event['start']['dateTime']:
            return event
    return None


def add_url_to_event(google_calendar_service, google_service, note_url, event, http_auth):
    google_request = google_calendar_service.add_url_to_event_description(google_service, note_url, event)

    return google_calendar_service.execute_request(google_request, http_auth)


"""
REFERENCE:
http://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
No build in function so I needed to see how I could catch the ValueError
"""


def date_formatted_correctly(date):
    try:
        datetime.strptime(date, "%d %B %Y")
        return True
    except ValueError:
        return False


def time_formatted_correctly(time):
    try:
        datetime.strptime(time, "%H:%S")
        return True
    except ValueError:
        return False
