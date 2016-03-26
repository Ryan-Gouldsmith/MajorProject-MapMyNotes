from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, send_file, safe_join, session
from werkzeug import secure_filename
from MapMyNotesApplication.models.file_upload_service import FileUploadService
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.exifparser import ExifParser

from MapMyNotesApplication.models.google_calendar_service import Google_Calendar_Service
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.oauth_service import Oauth_Service
import httplib2
from datetime import datetime, timedelta
import json
import os


fileupload = Blueprint('fileupload', __name__)

GET = "GET"
POST = "POST"
FILE_UPLOAD_PATH = "MapMyNotesApplication/upload/"

# Reference based upon but adapted to fit better into a more structured application.  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
@fileupload.route("/upload", methods=[GET,POST])
def file_upload_index_route():
    if request.method == POST:
        file = request.files["file"]
        if not file:
            return "A bad file has been uploaded"

        file_upload_service = FileUploadService()
        filename = file.filename

        if not file_upload_service.accepted_file_extension(filename):
            return "Error: Wrong file extention in uploaded file"

        if file_upload_service.is_forward_slash_in_filename(filename):
            filename = file_upload_service.prepare_file_path_file(filename)

        filename = secure_filename(filename)

        prepared_file = FILE_UPLOAD_PATH + filename

        file_upload_service.save_users_file(prepared_file, file)

        if not file_upload_service.file_exists(prepared_file):
            return "There was an error saving the file, please upload again."


        return redirect(url_for("fileupload.show_image", note_image=filename))

    return render_template('/file_upload/index.html')


@fileupload.route("/upload/show_image/<note_image>", methods=[GET])
def show_image(note_image):
    file_upload_service = FileUploadService()
    file_path = FILE_UPLOAD_PATH + note_image
    if not file_upload_service.file_exists(file_path):
        return redirect(url_for('fileupload.error_four_zero_four'))

    suggested_date = None
    events=None
    if not file_upload_service.is_png(file_path):
        exif_parser = ExifParser(file_path)
        exif_data = exif_parser.parse_exif()
        suggested_date = exif_parser.get_image_date()

    session_helper = SessionHelper()
    if session_helper.check_if_session_contains_credentials() is True:
        service = Oauth_Service()
        session_credentials = session_helper.return_session_credentials()
        credentials = service.create_credentials_from_json(session_credentials)
        http_auth = service.authorise(credentials, httplib2.Http())
        # https://developers.google.com/identity/protocols/OAuth2WebServer#example Reference for the access token expiration
        if credentials.access_token_expired is False and suggested_date is not None:
            suggested_date = datetime.strptime(suggested_date, "%Y:%m:%d %H:%M:%S")
            google_calendar_service = Google_Calendar_Service()
            google_service = google_calendar_service.build(http_auth)

            # Google requires it to be in  RFC 3339 format. http://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python Reference.
            # Additional reference on how to concat two date times so that I can start the date from midnight-almost mid-ngiht the next day. Modified for my own usage. http://stackoverflow.com/questions/9578906/easiest-way-to-combine-date-and-time-strings-to-single-datetime-object-using-pyt
            end_time = datetime.strptime('23:59', "%H:%M").time()
            start_time = datetime.strptime("00:00", "%H:%M").time()

            end_date = datetime.combine(suggested_date.date(), end_time).isoformat("T") + "Z"
            start_date = datetime.combine(suggested_date.date(), start_time ).isoformat("T") + "Z"
            print start_date
            print end_date
            #start_date = (datetime.utcnow() - timedelta(days=7)).isoformat("T") + "Z"
            google_request = google_calendar_service.get_list_of_events(google_service, start=start_date,end=end_date)

            google_calendar_response =  google_calendar_service.execute_request(google_request, http_auth)

            events = google_calendar_response['items']
        elif credentials.access_token_expired is True:
            return redirect(url_for("oauth.oauthsubmit"))


    return render_template("/file_upload/show_image.html",note_image=note_image, suggested_date=suggested_date, events=events)


# Not happy with this function, I think it will need to be looked into further down the down. Surely there's a better way than this. For some reason the send from directory did not work.... here https://github.com/mitsuhiko/flask/issues/1169
@fileupload.route("/img/<path:note_image>")
def get_image(note_image):
    file_upload_service = FileUploadService()
    file_path = FILE_UPLOAD_PATH + note_image
    if not file_upload_service.file_exists(file_path):
        return None

    filename = secure_filename(note_image)
    # TODO look for better way to fix this bug mentioned in the github issues
    application_root = os.path.dirname(fileupload.root_path)

    return send_from_directory(os.path.join(application_root, 'upload'), filename)


@fileupload.route("/error/404")
def error_four_zero_four():
    return render_template("/error/404.html")
