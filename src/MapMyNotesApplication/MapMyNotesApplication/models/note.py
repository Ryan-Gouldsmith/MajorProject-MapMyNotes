from MapMyNotesApplication import database
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.user import User
from sqlalchemy import Column, Integer, String, ForeignKey, and_


class Note(database.Model):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    image_path = Column(String(150), nullable=False)
    note_meta_data_id = Column(Integer, ForeignKey(NoteMetaData.id))
    calendar_url = Column(String(256))
    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, path, meta_data_id, user_id):
        self.image_path = path
        self.note_meta_data_id = meta_data_id
        self.user_id = user_id

    def save(self):
        if len(self.image_path) > 150:
            return False
        if self.calendar_url is not None and len(self.calendar_url) > 256:
            return False
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def update_meta_data_id(self, meta_data_id):
        """
        http://stackoverflow.com/questions/9667138/how-to-update-sqlalchemy-row-entry
        """
        self.note_meta_data_id = meta_data_id
        self.save()

    def update_calendar_url(self, calendar_url):
        self.calendar_url = calendar_url
        self.save()

    @staticmethod
    def find_note_by_module_code(module_code, user_id):
        # API REFERENCE : http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html#sqlalchemy.orm.query.Query.join
        query = ModuleCode.module_code.like(module_code)
        return Note.query.join(NoteMetaData.meta_data).join(NoteMetaData.module_code).filter(
            and_(Note.user_id == user_id, query)).all()
