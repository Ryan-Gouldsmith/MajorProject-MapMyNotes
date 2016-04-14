from flask import Blueprint, render_template, redirect, url_for

from MapMyNotesApplication.models.date_time_helper import DateTimeHelper
from MapMyNotesApplication.models.note import Note

shownote = Blueprint('shownote', __name__)

GET = "GET"
POST = "POST"


@shownote.route("/show_note/<note_id>", methods=[GET])
def show_note(note_id):
    note = Note.query.get(note_id)
    image_path = note.image_path
    module_code = note.meta_data.module_code.module_code
    lecturer = note.meta_data.lecturer
    location = note.meta_data.location

    calendar_url = None
    if note.calendar_url is not None:
        calendar_url = note.calendar_url

    formatted_date = DateTimeHelper.convert_date_time_to_string_representation(note.meta_data.date)

    title = note.meta_data.title
    return render_template('/show_note/index.html', note_image=image_path, module_code=module_code, lecturer=lecturer,
                           location=location, date=formatted_date, note_id=note.id, title=title,
                           calendar_url=calendar_url)


@shownote.route("/delete_note/<note_id>", methods=[POST])
def delete_note(note_id):
    note = Note.query.get(note_id)
    note.delete()
    #TODO delete from calendar too

    return redirect(url_for("homepage.home_page_route"))
