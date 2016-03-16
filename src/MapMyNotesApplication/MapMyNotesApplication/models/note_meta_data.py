from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String, ForeignKey, exc, DateTime, and_
from MapMyNotesApplication.models.module_code import Module_Code
from sqlalchemy.orm import relationship


class Note_Meta_Data(database.Model):

    __tablename__ = "notes_meta_data"
    id = Column(Integer, primary_key = True)
    lecturer = Column(String(100))
    location = Column(String(100))
    module_code_id = Column(Integer, ForeignKey(Module_Code.id))
    date = Column(DateTime)

    meta_data = relationship("Note", backref="meta_data")



    def __init__(self, lecturer_name, module_code, location, date):
        self.lecturer = lecturer_name
        self.module_code_id = module_code
        self.location = location
        self.date = date

    def save(self):
        if len(self.lecturer) > 100 or len(self.location) > 100:
            return False

        database.session.add(self)
        database.session.commit()
        return True

    def update_module_code_id(self, module_code_id):
        self.module_code_id = module_code_id
        self.save()
        

    @staticmethod
    def find_meta_data(meta_data):
        lecturer = meta_data.lecturer
        location = meta_data.location
        module_code = meta_data.module_code_id
        date = meta_data.date

        return Note_Meta_Data.query.filter(Note_Meta_Data.lecturer == lecturer, Note_Meta_Data.location == location, Note_Meta_Data.module_code_id == module_code, Note_Meta_Data.date == date).first()
