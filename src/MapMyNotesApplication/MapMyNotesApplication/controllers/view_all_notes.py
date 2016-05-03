from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.session_helper import SessionHelper
from flask import Blueprint, render_template, url_for, redirect, session

viewallnotes = Blueprint('viewallnotes', __name__)


@viewallnotes.route('/view_notes')
def view_all_notes():
    """
    Views all the notes in the system.
    """
    session_helper = SessionHelper(session)
    if session_helper.is_user_id_in_session() is False:
        return redirect(url_for('homepage.home_page_route'))

    user_id = session_helper.return_user_id()
    #find all notes for a given user
    notes = Note.query.filter(Note.user_id == user_id).all()
    return render_template("/view_all_notes/index.html", notes=notes)
