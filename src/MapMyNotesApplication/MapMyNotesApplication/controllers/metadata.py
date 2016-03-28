from flask import Blueprint, render_template, request, url_for, redirect, session
import httplib2
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from MapMyNotesApplication.models.oauth_service import Oauth_Service
import os
from datetime import datetime
from MapMyNotesApplication import database
from MapMyNotesApplication.models.session_helper import SessionHelper
metadata = Blueprint('metadata', __name__)


@metadata.route("/metadata/add/<note_image>", methods=["POST"])
def add_meta_data(note_image):
    if request.method == "POST":
        if check_all_params_exist(request.form) is False:
            return 'Some fields are missing'

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

            note = Note(note_image, note_meta_data.id)
            note.save()
            service = Oauth_Service()
            session_helper = SessionHelper()
            session_credentials = session_helper.return_session_credentials(session)
            credentials = service.create_credentials_from_json(session_credentials)
            http_auth = service.authorise(credentials, httplib2.Http())

            google_calendar_service = Google_Calendar_Service()
            note_url = google_calendar_service.prepare_url_for_event(note)
            google_service = google_calendar_service.build(http_auth)

            start_date = (date_time).isoformat("T") + "Z"
            end_time =  datetime.strptime('23:59', "%H:%M").time()

            end_date = datetime.combine(date_time.date(), end_time).isoformat("T") + "Z"

            google_request = google_calendar_service.get_list_of_events(google_service, start=start_date,end=end_date)

            google_calendar_response = google_calendar_service.execute_request(google_request, http_auth)
            module_code = module_code_obj.module_code
            saved = False
            for event in google_calendar_response['items']:
                if module_code in event['summary']:
                    google_request = google_calendar_service.add_url_to_event_description(google_service, note_url, event)
                    response = google_calendar_service.execute_request(google_request, http_auth)

                    if note_url in response['description']:
                        saved = True
                        note.update_calendar_url(response['htmlLink'])
            return redirect(url_for('shownote.show_note',note_id=note.id, saved=saved))
    return redirect(url_for('fileupload.error_four_zero_four'))


@metadata.route("/metadata/edit/<note_id>", methods=["GET", "POST"])
def edit_meta_data(note_id):
    if request.method == "GET":
        note = Note.query.get(note_id)
        module_code = note.meta_data.module_code.module_code
        lecturer = note.meta_data.lecturer
        location = note.meta_data.location
        date = note.meta_data.date.strftime("%d %B %Y %H:%M")
        title = note.meta_data.title

        return render_template('/file_upload/edit_meta_data.html', module_code=module_code, lecturer=lecturer, location=location, date=date, title=title)

    elif request.method == "POST":
        if not check_all_params_exist(request.form):
            return 'Some fields are missing'

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

    return True


def convert_string_date_to_datetime(date):
    return datetime.strptime(date, "%d %B %Y %H:%M")
