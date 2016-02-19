from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug import secure_filename
from MapMyNotesApplication.models.file_upload_service import FileUploadService

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

        file_upload_service.save_users_file(filename, file)

        return redirect(url_for("fileupload.show_note", note_image=filename))

    return render_template('/file_upload/index.html')

@fileupload.route("/upload/show_note/<note_image>", methods=["GET"])
def show_note(note_image):
    return "testing"
