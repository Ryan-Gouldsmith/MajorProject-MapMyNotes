from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String, ForeignKey
from MapMyNotesApplication.models.note_meta_data import Note_Meta_Data

class Note(database.Model):

    __tablename__ = "notes"
    id = Column(Integer, primary_key = True)
    image_path = Column(String(150))
    note_meta_data_id = Column(Integer, ForeignKey(Note_Meta_Data.id))


    def __init__(self, path, meta_data_id):
        self.image_path = path
        self.note_meta_data_id = meta_data_id

    def save(self):
        database.session.add(self)
        database.session.commit()
