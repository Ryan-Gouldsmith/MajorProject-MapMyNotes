import os

import httplib2
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename

from MapMyNotesApplication.models.binarise_image import BinariseImage
from MapMyNotesApplication.models.calendar_item import CalendarItem
from MapMyNotesApplication.models.date_time_helper import DateTimeHelper
from MapMyNotesApplication.models.exif_parser import ExifParser
from MapMyNotesApplication.models.file_upload_service import FileUploadService
from MapMyNotesApplication.models.google_calendar_service import GoogleCalendarService
from MapMyNotesApplication.models.google_services_helper import GoogleServicesHelper
from MapMyNotesApplication.models.oauth_service import OauthService
from MapMyNotesApplication.models.session_helper import SessionHelper
from MapMyNotesApplication.models.tesseract_helper import TesseractHelper

fileupload = Blueprint('fileupload', __name__)

GET = "GET"
POST = "POST"
FILE_UPLOAD_PATH = "MapMyNotesApplication/upload/"

"""
Reference based upon but adapted to fit better into a more structured application.
http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
"""


@fileupload.route("/upload", methods=[GET, POST])
def file_upload_index_route():
    session_helper = SessionHelper(session)
    if not session_helper.check_if_session_contains_credentials():
        return redirect(url_for('homepage.home_page_route'))
    if request.method == POST:
        uploaded_file = request.files["file"]
        if not uploaded_file:
            return "A bad file has been uploaded"

        filename = uploaded_file.filename
        file_upload_service = FileUploadService(filename)

        if not file_upload_service.accepted_file_extension():
            return "Error: Wrong file extension in uploaded file"

        if file_upload_service.is_forward_slash_in_filename():
            file_upload_service.remove_slash_from_filename()

        filename = secure_filename(file_upload_service.filename)
        file_upload_service.update_filename(filename)

        prepared_file = file_upload_service.add_full_path_to_filename(FILE_UPLOAD_PATH)
        file_upload_service.save_users_file(uploaded_file)

        binarise = BinariseImage()
        if binarise.image_file_exists(prepared_file):
            # TODO look into this, especially where return values are not used
            _ = binarise.read_image_as_grayscale(prepared_file)
            _ = binarise.apply_median_blur()
            threshold_image = binarise.apply_adaptive_threshold()
            horizontal_lines = binarise.copy_image(threshold_image)
            rows, columns = binarise.get_shape_info(horizontal_lines)
            structuring_element_kernel = binarise.get_structuring_element(75, 1)
            horizontal_lines = binarise.erode_image(horizontal_lines, structuring_element_kernel)
            horizontal_lines = binarise.dilate_image(horizontal_lines, structuring_element_kernel)

            horizontal_lines = binarise.dilate_image(horizontal_lines, structuring_element_kernel)

            _ = binarise.convert_black_threshold_to_white(horizontal_lines)

            new_mask = binarise.create_empty_mask(rows, columns)

            black_text_mask = binarise.convert_white_to_black(new_mask)

            one_kernel = binarise.create_kernels_of_ones(3, 3)

            dilated_black_text_mask = binarise.dilate_image(black_text_mask, one_kernel)

            _, _, _ = binarise.find_contours_in_mask(dilated_black_text_mask)

            dilated_black_text_mask = binarise.draw_contours(dilated_black_text_mask)

            ones_kernel = binarise.create_kernels_of_ones(7, 7)

            final_output = binarise.erode_image(dilated_black_text_mask, ones_kernel)

            _ = binarise.prepare_image_to_save(prepared_file)

            binarise.save_image(final_output)

        if not file_upload_service.file_exists():
            return "There was an error saving the file, please upload again."

        return redirect(url_for("fileupload.show_image", note_image=filename))

    return render_template('/file_upload/index.html')


@fileupload.route("/upload/show_image/<note_image>", methods=[GET])
def show_image(note_image):
    file_upload_service = FileUploadService(note_image)
    file_upload_service.add_full_path_to_filename(FILE_UPLOAD_PATH)
    errors = None
    session_helper = SessionHelper(session)
    if session_helper.errors_in_session():
        errors = session_helper.get_errors()
        session_helper.delete_session_errors()

    if not file_upload_service.file_exists():
        return redirect(url_for('fileupload.error_four_zero_four'))

    suggested_date = None
    events = None
    if not file_upload_service.is_png():
        exif_parser = ExifParser(file_upload_service.upload_path)
        # TODO does it need to return a value here?
        _ = exif_parser.parse_exif()
        suggested_date = exif_parser.get_image_date()

    if session_helper.check_if_session_contains_credentials():
        credentials, http_auth = GoogleServicesHelper.authorise(session_helper)
        """
        https://developers.google.com/identity/protocols/OAuth2WebServer#example
        Reference for the access token expiration
        """
        if not credentials.access_token_expired and suggested_date is not None:
            google_calendar_service = GoogleCalendarService()
            google_service = google_calendar_service.build(http_auth)

            """
            Google requires it to be in  RFC 3339 format.
            http://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python Reference.
            Additional reference on how to concat two date times
            I can start the date from midnight-almost mid-night the next day.
            Modified for my own usage.
            http://stackoverflow.com/questions/9578906/easiest-way-to-combine-date-and-time-strings-to-single-datetime-object-using-pyt
            """
            date_time_helper = DateTimeHelper()
            suggested_date, end_date, start_date = date_time_helper.process_suggested_date_for_calendar_events(
                suggested_date)
            google_request = google_calendar_service.get_list_of_events(google_service, start=start_date, end=end_date)

            google_calendar_response = google_calendar_service.execute_request(google_request, http_auth)

            cal_events = google_calendar_response['items']
            events = []
            for event in cal_events:
                event = CalendarItem(event)
                events.append(event)

        elif credentials.access_token_expired:
            return redirect(url_for('logout.logout'))

    # TESSERACT PARSING HERE
    filename_test, file_extension = os.path.splitext(note_image)
    tiff_image = filename_test + ".tif"
    tif_path = FILE_UPLOAD_PATH + tiff_image

    tesseract_helper = TesseractHelper(tif_path)
    tesseract_helper.set_tiff_image_for_analysis()
    _ = tesseract_helper.get_confidence_and_words_from_image()

    tesseract_module_code = tesseract_helper.get_module_code_line()
    tesseract_title = tesseract_helper.get_title_line()
    tesseract_date = tesseract_helper.get_date_line()
    tesseract_lecturer = tesseract_helper.get_lecturer_line()

    """
    Reference for empty string regex
    http://stackoverflow.com/questions/406230/regular-expression-to-match-line-that-doesnt-contain-a-word
    Used this tool to help to create my own too:
    http://regexr.com/
    """
    return render_template("/file_upload/show_image.html", note_image=note_image, suggested_date=suggested_date,
                           events=events, tesseract_module_code=tesseract_module_code, tesseract_title=tesseract_title,
                           tesseract_date=tesseract_date, tesseract_lecturer=tesseract_lecturer, errors=errors)


"""
    Not happy with this function, I think it will need to be looked into further down the down.
    Surely there's a better way than this.
    For some reason the send from directory did not work.
    here https://github.com/mitsuhiko/flask/issues/1169
"""


@fileupload.route("/img/<path:note_image>")
def get_image(note_image):
    file_upload_service = FileUploadService(note_image)
    file_upload_service.add_full_path_to_filename(FILE_UPLOAD_PATH)
    if not file_upload_service.file_exists():
        return None

    filename = secure_filename(note_image)
    application_root = os.path.dirname(fileupload.root_path)

    return send_from_directory(os.path.join(application_root, 'upload'), filename)


@fileupload.route("/error/404")
def error_four_zero_four():
    return render_template("/error/404.html")
