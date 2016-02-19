from flask import Blueprint, render_template, request
from werkzeug import secure_filename
from MapMyNotesApplication.models.file_upload_service import FileUploadService

fileupload = Blueprint('fileupload', __name__)

# Reference based upon but adapted to fit better into a more structured application.  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
@fileupload.route("/upload", methods=["GET", "POST"])
def file_upload_index_route():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "bad file"

        file_upload_service = FileUploadService()
        filename = file.filename
        if file_upload_service.is_forward_slash_in_filename(filename):
            filename = file_upload_service.prepare_file_path_file(filename)


        filename = secure_filename(filename)

        file_upload_service.save_users_file(filename, file)

    return render_template('/file_upload/index.html')
