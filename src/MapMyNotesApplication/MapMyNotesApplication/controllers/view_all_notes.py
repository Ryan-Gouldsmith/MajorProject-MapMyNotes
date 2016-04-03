from flask import Blueprint, render_template, request, url_for, redirect, current_app, session
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.session_helper import SessionHelper

viewallnotes = Blueprint('viewallnotes', __name__)


@viewallnotes.route('/view_notes')
def view_all_notes():
    session_helper = SessionHelper()
    if session_helper.is_user_id_in_session(session) is False:
        return redirect(url_for('homepage.home_page_route'))

    user_id = session_helper.return_user_id(session)
    print user_id
    notes = Note.query.filter(Note.user_id == user_id).all()
    return render_template("/view_all_notes/index.html", notes=notes)
