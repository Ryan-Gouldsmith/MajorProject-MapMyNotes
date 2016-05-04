from flask import Blueprint, render_template, request, url_for, redirect, session

from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.session_helper import SessionHelper

searchblueprint = Blueprint('searchblueprint', __name__)

GET = 'GET'


@searchblueprint.route("/search", methods=[GET])
def search():
    """
    API route for helping to search for a given module code
    """
    session_helper = SessionHelper(session)
    if session_helper.is_user_id_in_session() is False:
        return redirect(url_for('homepage.home_page_route'))

    if request.args:
        #attempts to get the query string module code
        module_code = request.args.get('module_code').upper()
        user_id = session_helper.return_user_id()
        #finds all notes
        notes = Note.find_note_by_module_code(module_code, user_id)
        return render_template("search/show_notes.html", notes=notes, searched=module_code)

    return render_template("search/index.html")
