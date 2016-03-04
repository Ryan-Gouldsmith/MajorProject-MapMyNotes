from flask import Blueprint, render_template, request
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note import Note

shownote = Blueprint('shownote', __name__)

@shownote.route("/show_note/<note_id>", methods=["GET"])
def show_note(note_id):

    note = Note.query.get(note_id)

    image_path = note.image_path
    module_code = note.module_code.module_code
    return render_template('/show_note/index.html', note_image=image_path, module_code=module_code)
