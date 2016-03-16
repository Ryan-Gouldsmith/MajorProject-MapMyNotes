from flask import Blueprint, render_template, request, url_for, redirect
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data
import os
from datetime import datetime
from MapMyNotesApplication import database
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
        if request.form['date_data'] is None:
            return "Failed to submit date data"


        module_code_data = request.form['module_code_data'].upper()

        lecturer_name_data = request.form['lecturer_name_data']

        location_data = request.form['location_data']

        date_data = request.form['date_data']

        file_path = "MapMyNotesApplication/upload/" + note_image

        if module_code_data and os.path.isfile(file_path):
            module_code_obj = Module_Code.find_id_by_module_code(module_code_data)
            if module_code_obj is None:
                module_code_obj = Module_Code(module_code_data)
                module_code_obj.save()


            module_code_id = module_code_obj.id

            date_time = datetime.strptime(date_data, "%dth %B %Y %H:%M")


            note_meta_data = Note_Meta_Data(lecturer_name_data, module_code_id, location_data, date_time)
            note_meta_data.save()


            note = Note(note_image, note_meta_data.id)
            note.save()
            return redirect(url_for('shownote.show_note',note_id=note.id))



    return redirect(url_for('fileupload.error_four_zero_four'))


@metadata.route("/metadata/edit/<note_id>", methods=["GET", "POST"])
def edit_meta_data(note_id):
    if request.method == "GET":
        note = Note.query.get(note_id)
        module_code = note.meta_data.module_code.module_code
        lecturer = note.meta_data.lecturer
        location = note.meta_data.location
        date = note.meta_data.date.strftime("%dth %B %Y %H:%M")

        return render_template('/file_upload/edit_meta_data.html', module_code=module_code, lecturer=lecturer, location=location, date=date)
    elif request.method == "POST":
        if request.form['module_code_data'] is None:
            return "Failed to submit module code data"
        if request.form['lecturer_name_data'] is None:
            return "Failed to submit lecturer name data"
        if request.form['location_data'] is None:
            return "Failed to submit the location"
        if request.form['date_data'] is None:
            return "Failed to submit date data"

        module_code_data = request.form['module_code_data'].upper()

        lecturer_name= request.form['lecturer_name_data']

        location = request.form['location_data']

        date = request.form['date_data']

        module_code = Module_Code.find_id_by_module_code(module_code_data)

        if module_code is not None:
            module_code_id = module_code.id
            date_time = datetime.strptime(date, "%dth %B %Y %H:%M")

            meta_data = Note_Meta_Data(lecturer_name, module_code_id, location, date_time)


            found_meta_data = Note_Meta_Data.find_meta_data(meta_data)
            note = Note.query.get(note_id)
            print found_meta_data
            if found_meta_data is not None:
                note.note_meta_data_id = found_meta_data.id
                database.session.commit()
            else:
                meta_data.save()
                note.note_meta_data_id = meta_data.id
                database.session.commit()

        else:
            #create a new Note
            module_code_obj = Module_Code(module_code_data)
            module_code_obj.save()
            module_code_id = module_code_obj.id



            date_time = datetime.strptime(date, "%dth %B %Y %H:%M")


            note_meta_data = Note_Meta_Data(lecturer_name, module_code_id, location, date_time)
            response = note_meta_data.save()

            note = Note.query.get(note_id)
            #http://stackoverflow.com/questions/9667138/how-to-update-sqlalchemy-row-entry
            note.note_meta_data_id = note_meta_data.id
            database.session.commit()

        return "success"
