from flask import Blueprint, render_template, request, url_for, redirect, session
import httplib2
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from MapMyNotesApplication.models.oauth_service import Oauth_Service
from MapMyNotesApplication.models.user import User
import os
from datetime import datetime
from MapMyNotesApplication import database
from MapMyNotesApplication.models.session_helper import SessionHelper
from dateutil import parser, tz

metadata = Blueprint('metadata', __name__)


@metadata.route("/metadata/add/<note_image>", methods=["POST"])
def add_meta_data(note_image):
    session_helper = SessionHelper()
    if session_helper.is_user_id_in_session(session) is False:
        return redirect(url_for('homepage.home_page_route'))

    if request.method == "POST":
        if check_all_params_exist(request.form) is False:
            session['errors'] = "Some fields are missing"
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        if date_formatted_correctly(request.form['date_data']) is False:
            session['errors'] = "Wrong date format: should be date month year hour:minute, eg: 20 February 2016 16:00"
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        module_code_data = request.form['module_code_data'].upper()

        lecturer_name_data = request.form['lecturer_name_data']

        location_data = request.form['location_data']

        date_data = request.form['date_data']

        title_data = request.form['title_data']

        file_path = "MapMyNotesApplication/upload/" + note_image

        if module_code_data and os.path.isfile(file_path):
            module_code_obj = Module_Code.find_id_by_module_code(module_code_data)
            if module_code_obj is None:
                module_code_obj = Module_Code(module_code_data)
                module_code_obj.save()

            module_code_id = module_code_obj.id
            date_time = convert_string_date_to_datetime(date_data)
            note_meta_data = Note_Meta_Data(lecturer_name_data, module_code_id, location_data, date_time, title_data)
            note_meta_data.save()

            user_id = session_helper.return_user_id(session)
            user = User.query.get(user_id)
            note = Note(note_image, note_meta_data.id, user.id)
            note.save()

            service = Oauth_Service()
            session_credentials = session_helper.return_session_credentials(session)
            credentials = service.create_credentials_from_json(session_credentials)
            http_auth = service.authorise(credentials, httplib2.Http())

            google_calendar_service = Google_Calendar_Service()
            note_url = google_calendar_service.prepare_url_for_event(note)
            google_service = google_calendar_service.build(http_auth)

            start_date, end_date = process_time_zone(date_time)
            google_request = google_calendar_service.get_list_of_events(google_service, start=start_date,end=end_date)

            google_calendar_response = google_calendar_service.execute_request(google_request, http_auth)
            module_code = module_code_obj.module_code

            event = get_event_containing_module_code(module_code, google_calendar_response, start_date)

            saved_response = None
            if event is not None:
                saved_response = add_url_to_event(google_calendar_service, google_service, note_url, event, http_auth)

            if saved_response is not None and note_url in saved_response['description']:
                note.update_calendar_url(saved_response['htmlLink'])

            return redirect(url_for('shownote.show_note',note_id=note.id))
    return redirect(url_for('fileupload.error_four_zero_four'))


@metadata.route("/metadata/edit/<note_id>", methods=["GET", "POST"])
def edit_meta_data(note_id):
    if request.method == "GET":
        errors = None
        session_helper = SessionHelper()
        if session_helper.errors_in_session(session):
            errors = session_helper.get_errors(session)
            session_helper.delete_session_errors(session)

        note = Note.query.get(note_id)
        module_code = note.meta_data.module_code.module_code
        lecturer = note.meta_data.lecturer
        location = note.meta_data.location
        date = note.meta_data.date.strftime("%d %B %Y %H:%M")
        title = note.meta_data.title

        return render_template('/file_upload/edit_meta_data.html', module_code=module_code, lecturer=lecturer, location=location, date=date, title=title, note_image=note.image_path, errors=errors)

    elif request.method == "POST":
        if check_all_params_exist(request.form) is False:
            session['errors'] = "Some fields are missing"
            return redirect(url_for('metadata.edit_meta_data', note_id=note_id))

        if date_formatted_correctly(request.form['date_data']) is False:
            session['errors'] = "Wrong date format: should be date month year hour:minute, eg: 20 February 2016 16:00"
            return redirect(url_for('metadata.edit_meta_data', note_id=note_id))

        module_code_data = request.form['module_code_data'].upper()

        lecturer_name= request.form['lecturer_name_data']

        location = request.form['location_data']

        date = request.form['date_data']

        title = request.form['title_data']

        module_code = Module_Code.find_id_by_module_code(module_code_data)
        date_time = convert_string_date_to_datetime(date)

        if module_code is not None:
            meta_data = Note_Meta_Data(lecturer_name, module_code.id, location, date_time, title)

            found_meta_data = Note_Meta_Data.find_meta_data(meta_data)

            note = Note.query.get(note_id)
            if found_meta_data is not None:
                note.update_meta_data_id(found_meta_data.id)
            else:
                meta_data.save()
                note.update_meta_data_id(meta_data.id)
        else:
            module_code_obj = Module_Code(module_code_data)
            module_code_obj.save()

            note_meta_data = Note_Meta_Data(lecturer_name, module_code_obj.id, location, date_time, title)
            response = note_meta_data.save()

            note = Note.query.get(note_id)
            note.update_meta_data_id(note_meta_data.id)

        return redirect(url_for('shownote.show_note',note_id=note_id))


def check_all_params_exist(params):
    if params["module_code_data"] is None or params['lecturer_name_data'] is None or params['location_data'] is None or params['date_data'] is None or params['title_data'] is None:
        return False

    # REFERENCE isspace checks for empty spaces http://stackoverflow.com/questions/2405292/how-to-check-if-text-is-empty-spaces-tabs-newlines-in-python

    if params['module_code_data'].isspace() or params['lecturer_name_data'].isspace() or params['location_data'].isspace() or params['date_data'].isspace() or params['title_data'].isspace():
        return False

    return True


def convert_string_date_to_datetime(date):
    return datetime.strptime(date, "%d %B %Y %H:%M")


def process_time_zone(date_time):
    """ Great API
    https://docs.python.org/2/library/datetime.html#datetime.datetime.replace
    Had issue with the BST. Had to supply the timezone offset to Google API.
    """
    date_time = date_time.replace(tzinfo=tz.gettz('Europe/London'))
    start_date = (date_time).isoformat("T")
    end_time = datetime.strptime('23:59', "%H:%M").time()
    end_date = datetime.combine(date_time.date(), end_time)
    end_date = end_date.replace(tzinfo=tz.gettz('Europe/London'))
    end_date = end_date.isoformat("T")
    return start_date, end_date


def get_event_containing_module_code(module_code, calendar_response, start_date):
    for event in calendar_response["items"]:
        if module_code in event['summary'] and start_date == event['start']['dateTime']:
            return event
    return None

def add_url_to_event(google_calendar_service, google_service, note_url, event, http_auth):
    google_request = google_calendar_service.add_url_to_event_description(google_service, note_url, event)

    return google_calendar_service.execute_request(google_request, http_auth)

"""
REFERENCE: http://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python No build in function so I needed to see how I could catch the ValueError
"""
def date_formatted_correctly(date):
    try:
        datetime.strptime(date, "%d %B %Y %H:%M")
        return True
    except ValueError:
        return False
