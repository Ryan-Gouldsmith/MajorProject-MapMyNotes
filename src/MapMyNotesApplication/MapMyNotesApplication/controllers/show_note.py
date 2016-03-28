from flask import Blueprint, render_template, request, redirect, url_for
from MapMyNotesApplication.models.module_code import Module_Code
from MapMyNotesApplication.models.note import Note
from datetime import datetime

shownote = Blueprint('shownote', __name__)

@shownote.route("/show_note/<note_id>", methods=["GET"])
def show_note(note_id):

    note = Note.query.get(note_id)

    image_path = note.image_path
    module_code = note.meta_data.module_code.module_code

    lecturer = note.meta_data.lecturer

    location = note.meta_data.location

    #TODO replace this with an attribute in the db
    saved = request.args.get('saved')
    calendar_url = note.calendar_url

    date = note.meta_data.date
    formated_date = date.strftime("%d %B %Y %H:%M")

    title = note.meta_data.title

    note_id = note.id
    return render_template('/show_note/index.html', note_image=image_path, module_code=module_code, lecturer=lecturer, location=location, date=formated_date, note_id=note_id, title=title, saved=saved, calendar_url=calendar_url)

@shownote.route("/delete_note/<note_id>", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get(note_id)

    note.delete()

    return redirect(url_for("homepage.home_page_route"))
