from MapMyNotesApplication.models.note import Note
from flask import Blueprint, render_template, redirect, url_for

shownote = Blueprint('shownote', __name__)


@shownote.route("/show_note/<note_id>", methods=["GET"])
def show_note(note_id):
    note = Note.query.get(note_id)

    image_path = note.image_path
    module_code = note.meta_data.module_code.module_code

    lecturer = note.meta_data.lecturer

    location = note.meta_data.location

    calendar_url = None
    if note.calendar_url is not None:
        calendar_url = note.calendar_url

    date = note.meta_data.date
    formatted_date = date.strftime("%d %B %Y %H:%M")

    title = note.meta_data.title

    note_id = note.id
    return render_template('/show_note/index.html', note_image=image_path, module_code=module_code, lecturer=lecturer,
                           location=location, date=formatted_date, note_id=note_id, title=title,
                           calendar_url=calendar_url)


@shownote.route("/delete_note/<note_id>", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get(note_id)

    note.delete()

    return redirect(url_for("homepage.home_page_route"))
