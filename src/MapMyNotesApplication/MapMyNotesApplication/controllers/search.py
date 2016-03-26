from flask import Blueprint, render_template, request, url_for, redirect, current_app, session

searchblueprint =  Blueprint('searchblueprint', __name__)
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.module_code import Module_Code


@searchblueprint.route("/search/<module_code>", methods=["GET"])
def search_module_code(module_code):
    return "success"

@searchblueprint.route("/search", methods=["GET"])
def search():
    if request.args:
        module_code = request.args.get('module_code')
        notes = Note.find_note_by_module_code(module_code)
        return render_template("search/show_notes.html", notes=notes, searched=module_code)

    return render_template("search/index.html")
