from flask import Blueprint, render_template, request, url_for, redirect, current_app, session
from MapMyNotesApplication.models.note import Note

viewallnotes = Blueprint('viewallnotes', __name__)

@viewallnotes.route('/view_notes')
def view_all_notes():
    notes = Note.query.all()
    return render_template("/view_all_notes/index.html", notes=notes)
