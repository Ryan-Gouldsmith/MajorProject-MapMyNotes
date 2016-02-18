from flask import Blueprint, render_template, request
fileupload = Blueprint('fileupload', __name__)


@fileupload.route("/upload", methods=["GET", "POST"])
def file_upload_index_route():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "bad file"

        #file.save("tests/test_image_upload.jpg")

    return render_template('/file_upload/index.html')
