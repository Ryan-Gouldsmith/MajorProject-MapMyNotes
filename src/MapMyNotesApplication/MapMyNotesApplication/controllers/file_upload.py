from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, send_file, safe_join
from werkzeug import secure_filename
from MapMyNotesApplication.models.file_upload_service import FileUploadService
from MapMyNotesApplication.models.note import Note
import os


fileupload = Blueprint('fileupload', __name__)

# Reference based upon but adapted to fit better into a more structured application.  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
@fileupload.route("/upload", methods=["GET", "POST"])
def file_upload_index_route():
    if request.method == "POST":
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
        note = Note(filename)
        note.save()


        file_upload_service.save_users_file(filename, file)

        return redirect(url_for("fileupload.show_note", note_image=filename))

    return render_template('/file_upload/index.html')


@fileupload.route("/upload/show_note/<note_image>", methods=["GET"])
def show_note(note_image):
    file_exists = os.path.isfile('MapMyNotesApplication/upload/'+note_image)
    if not file_exists:
        return redirect(url_for('fileupload.error_four_zero_four'))

    return render_template("/file_upload/show_note.html",note_image=note_image)


# Not happy with this function, I think it will need to be looked into further down the down. Surely there's a better way than this. For some reason the send from directory did not work.... here https://github.com/mitsuhiko/flask/issues/1169
@fileupload.route("/img/<path:note_image>")
def get_image(note_image):
    file_exists = os.path.isfile('MapMyNotesApplication/upload/'+note_image)
    filename = secure_filename(note_image)
    # TODO look for better way to fix this bug mentioned in the github issues
    application_root = os.path.dirname(fileupload.root_path)
    return send_from_directory(os.path.join(application_root, 'upload'), filename)


@fileupload.route("/error/404")
def error_four_zero_four():
    return render_template("/error/404.html")
