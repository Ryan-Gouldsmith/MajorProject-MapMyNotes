from flask import Blueprint, render_template, request, url_for, redirect
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
import os
metadata = Blueprint('metadata', __name__)

@metadata.route("/metadata/add/<note_image>", methods=["POST"])
def add_meta_data(note_image):
    if request.method == "POST":
        if request.form['module_code_data'] is None:
            return "Failed to submit module code data"
        if request.form['lecturer_name_data'] is None:
            return "Failed to submit lecturer name data"
        if request.form['location_data'] is None:
            return "Failed to submit the location"

        module_code_data = request.form['module_code_data'].upper()

        lecturer_name_data = request.form['lecturer_name_data']

        location_data = request.form['location_data']

        file_path = "MapMyNotesApplication/upload/" + note_image

        if module_code_data and os.path.isfile(file_path):
            module_code_obj = Module_Code.find_id_by_module_code(module_code_data)
            if module_code_obj is None:
                module_code_obj = Module_Code(module_code_data)
                module_code_obj.save()


            module_code_id = module_code_obj.id

            note_meta_data = Note_Meta_Data(lecturer_name_data, module_code_id, location_data)
            note_meta_data.save()


            note = Note(note_image, note_meta_data.id)
            note.save()
            return redirect(url_for('shownote.show_note',note_id=note.id))



    return redirect(url_for('fileupload.error_four_zero_four'))
