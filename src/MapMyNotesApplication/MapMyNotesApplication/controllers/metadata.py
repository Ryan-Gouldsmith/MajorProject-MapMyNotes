import os

from flask import Blueprint, render_template, request, url_for, redirect, session

from MapMyNotesApplication.models.date_time_helper import DateTimeHelper
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.google_services_helper import GoogleServicesHelper
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.user import User

metadata = Blueprint('metadata', __name__)

POST = "POST"
GET = "GET"


@metadata.route("/metadata/add/<note_image>", methods=[POST])
def add_meta_data(note_image):
    session_helper = SessionHelper(session)
    if not session_helper.is_user_id_in_session():
        return redirect(url_for('homepage.home_page_route'))

    credentials, http_auth = GoogleServicesHelper.authorise(session_helper)

    if credentials.access_token_expired:
        return redirect(url_for('logout.logout'))

    if request.method == POST:
        if not check_all_params_exist(request.form):
            error = "Some fields are missing"
            session_helper.set_errors_in_session(error)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        date = request.form['date_data']
        time = request.form['time_data']
        date_time_helper = DateTimeHelper(date, time)

        if not date_time_helper.is_date_formatted_correctly():
            error = "Wrong date format: should be date month year hour:minute, eg: 20 February 2016"
            session_helper.set_errors_in_session(error)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        if not date_time_helper.is_time_formatted_correctly():
            error = "Wrong time format: should be hour:minute, e.g 13:00"
            session_helper.set_errors_in_session(error)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        any_errors, errors = check_all_params_are_less_than_schema_length(request.form)
        if any_errors:
            session_helper.set_errors_in_session(errors)
            return redirect(url_for('fileupload.show_image', note_image=note_image))

        module_code_data = request.form['module_code_data'].upper()
        lecturer_name_data = request.form['lecturer_name_data']
        location_data = request.form['location_data']
        title_data = request.form['title_data']

        file_path = "MapMyNotesApplication/upload/" + note_image

        if module_code_data and os.path.isfile(file_path):
            module_code_obj = ModuleCode.find_id_by_module_code(module_code_data)
            if module_code_obj is None:
                module_code_obj = ModuleCode(module_code_data)
                module_code_obj.save()

            module_code_id = module_code_obj.id
            date_time = date_time_helper.convert_string_date_and_time_to_datetime()
            note_meta_data = NoteMetaData(lecturer_name_data, module_code_id, location_data, date_time, title_data)
            note_meta_data.save()

            user_id = session_helper.return_user_id()
            user = User.query.get(user_id)
            note = Note(note_image, note_meta_data.id, user.id)
            note.save()

            google_calendar_service = GoogleCalendarService()
            google_service = google_calendar_service.build(http_auth)

            note_url = google_calendar_service.prepare_url_for_event(note)
            date_time_helper = DateTimeHelper(combined_date_time=date_time)
            start_date, end_date = date_time_helper.process_time_zone()
            google_calendar_response = google_calendar_service.get_events_based_on_date(start_date, end_date, http_auth,
                                                                                        google_service)

            module_code = module_code_obj.module_code

            event = GoogleServicesHelper.get_event_containing_module_code(module_code, google_calendar_response,
                                                                          date_time)

            saved_response = None
            if event is not None:
                saved_response = google_calendar_service.add_url_to_event_description(google_service, note_url, event,
                                                                                      http_auth)

            if saved_response is not None and note_url in saved_response['description']:
                note.update_calendar_url(saved_response['htmlLink'])

            return redirect(url_for('shownote.show_note', note_id=note.id))
    return redirect(url_for('fileupload.error_four_zero_four'))


@metadata.route("/metadata/edit/<note_id>", methods=[GET, POST])
def edit_meta_data(note_id):
    session_helper = SessionHelper(session)
    credentials, http_auth = GoogleServicesHelper.authorise(session_helper)

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
        time, date = DateTimeHelper.convert_datetime_to_string_date_and_time(note.meta_data.date)
        title = note.meta_data.title

        return render_template('/file_upload/edit_meta_data.html', module_code=module_code, lecturer=lecturer,
                               location=location, date=date, time=time, title=title, note_image=note.image_path,
                               errors=errors)

    elif request.method == POST:
        note = Note.query.get(note_id)
        previous_date = note.meta_data.date

        google_calendar_service = GoogleCalendarService()
        google_service = google_calendar_service.build(http_auth)
        date_time_helper = DateTimeHelper(combined_date_time=previous_date)
        start_date, end_date = date_time_helper.process_time_zone()
        note_url = google_calendar_service.prepare_url_for_event(note)
        google_calendar_response = google_calendar_service.get_events_based_on_date(start_date, end_date, http_auth,
                                                                                    google_service)

        module_code = note.meta_data.module_code.module_code

        event = GoogleServicesHelper.get_event_containing_module_code(module_code, google_calendar_response,
                                                                      previous_date)
        if event and 'description' in note_url and note_url in event['description']:
            response = google_calendar_service.add_url_to_event_description(google_service, "", event,
                                                                            http_auth)

        if not check_all_params_exist(request.form):
            session['errors'] = "Some fields are missing"
            return redirect(url_for('metadata.edit_meta_data', note_id=note_id))

        date = request.form['date_data']
        time = request.form['time_data']
        date_time_helper = DateTimeHelper(date, time)

        if not date_time_helper.is_date_formatted_correctly():
            session['errors'] = "Wrong date format: should be date month year eg: 20 February 2016"
            return redirect(url_for('metadata.edit_meta_data', note_id=note_id))

        if not date_time_helper.is_time_formatted_correctly():
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
        title = request.form['title_data']
        module_code = ModuleCode.find_id_by_module_code(module_code_data)
        date_time = date_time_helper.convert_string_date_and_time_to_datetime()

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
            note_meta_data.save()

            note = Note.query.get(note_id)
            note.update_meta_data_id(note_meta_data.id)

        note_url = google_calendar_service.prepare_url_for_event(note)
        date_time_helper = DateTimeHelper(combined_date_time=previous_date)
        start_date, end_date = date_time_helper.process_time_zone()
        google_calendar_response = google_calendar_service.get_events_based_on_date(start_date, end_date, http_auth,
                                                                                    google_service)

        event = GoogleServicesHelper.get_event_containing_module_code(module_code.module_code, google_calendar_response,
                                                                      date_time)
        if event:
            response = google_calendar_service.add_url_to_event_description(google_service, note_url, event,
                                                                            http_auth)
            if response is not None and note_url in response['description']:
                note.update_calendar_url(response['htmlLink'])

        return redirect(url_for('shownote.show_note', note_id=note_id))


# TODO: Move the below functions to a helper class?

def check_all_params_exist(params):
    if params["module_code_data"] is None or params['lecturer_name_data'] is None or params['location_data'] is None \
            or params['date_data'] is None or params['title_data'] is None or params['time_data'] is None:
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
