from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os
from models.testimage import TestImage

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def homepage():
    #Reference:http://flask.pocoo.org/docs/0.10/patterns/fileuploads/#uploading-files
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("static/", filename))
            return redirect(url_for('invert_image', filename = filename))


    return render_template("homepage.html")


@app.route("/invert/<filename>", methods=["GET"])
def invert_image(filename):
    testimage = TestImage()
    modified_file = testimage.binarise_image(filename)

    return render_template('show.html', filename = filename, modified = modified_file)




if __name__ == '__main__':
    app.run(debug=True)
