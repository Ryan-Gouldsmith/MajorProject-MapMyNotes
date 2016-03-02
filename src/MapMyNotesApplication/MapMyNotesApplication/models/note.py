from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String

class Note(database.Model):

    __tablename__ = "notes"
    id = Column(Integer, primary_key = True)
    image_path = Column(String(150))


    def __init__(self, path):
        self.image_path = path

    def save(self):
        database.session.add(self)
        database.session.commit()
