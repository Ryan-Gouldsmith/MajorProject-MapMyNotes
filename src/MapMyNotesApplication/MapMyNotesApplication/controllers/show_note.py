from flask import Blueprint, render_template, request
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note import Note

shownote = Blueprint('shownote', __name__)

@shownote.route("/show_note/<note_id>", methods=["GET"])
def show_note(note_id):

    note = Note.query.get(note_id)

    image_path = note.image_path
    module_code = note.meta_data.module_code.module_code

    lecturer = note.meta_data.lecturer

    location = note.meta_data.location
    return render_template('/show_note/index.html', note_image=image_path, module_code=module_code, lecturer=lecturer, location=location)
