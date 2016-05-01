from datetime import datetime

from flask.ext.testing import TestCase

from MapMyNotesApplication import application, database, csrf
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note import Note
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.user import User


class TestIntegrationShowNote(TestCase):
    def create_app(self):
        application.config['TESTING'] = True
        app = application
        csrf.init_app(app)
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/
        # Used to help with the test database, maybe could move this to a config file..

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

        module_code = ModuleCode('CS31310')
        database.session.add(module_code)
        database.session.commit()
        self.module_code_id = module_code.id

        date = datetime.strptime("20 January 2016 15:00", "%d %B %Y %H:%M")
        note_meta_data = NoteMetaData("Mr Foo", self.module_code_id, 'C11 Hugh Owen', date, "Title")
        note_meta_data.save()
        self.note_meta_data_id = note_meta_data.id

        user = User("test@gmail.com")
        database.session.add(user)
        database.session.commit()
        self.user_id = user.id

        with self.client.session_transaction() as session:
            session['user_id'] = self.user_id

        file_list = 'tests/test.png'.split("/")

        self.image = file_list[1]

    def test_route_returns_status_code_200(self):
        note = Note('uploads/', self.note_meta_data_id, self.user_id)
        note.save()

        response = self.client.get('/show_note/1')
        assert response.status_code == 200

    def test_deleting_a_note_returns_status_code_200(self):
        note = Note('uploads/', self.note_meta_data_id, self.user_id)
        note.save()

        resource = self.client.post('/delete_note/' + str(note.id))

        assert resource.status_code == 302

    def test_deleting_a_note_deletes_a_note_from_database(self):
        note = Note('uploads/', self.note_meta_data_id, self.user_id)
        note.save()

        resource = self.client.post('/delete_note/' + str(note.id))

        notes = Note.query.all()

        assert len(notes) is 0
