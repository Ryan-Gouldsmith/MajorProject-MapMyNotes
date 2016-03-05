from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String, ForeignKey, exc, DateTime
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
