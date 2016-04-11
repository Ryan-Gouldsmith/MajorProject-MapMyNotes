from MapMyNotesApplication import database
from MapMyNotesApplication.models.module_code import ModuleCode
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class NoteMetaData(database.Model):
    __tablename__ = "notes_meta_data"
    id = Column(Integer, primary_key=True)
    lecturer = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    module_code_id = Column(Integer, ForeignKey(ModuleCode.id))
    date = Column(DateTime, nullable=False)
    title = Column(String(100), nullable=False)

    meta_data = relationship("Note", backref="meta_data")

    def __init__(self, lecturer_name, module_code, location, date, title):
        self.lecturer = lecturer_name
        self.module_code_id = module_code
        self.location = location
        self.date = date
        self.title = title

    def save(self):
        if len(self.lecturer) > 100 or len(self.location) > 100 or len(self.title) > 100:
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

        return NoteMetaData.query.filter(NoteMetaData.lecturer == lecturer, NoteMetaData.location == location,
                                         NoteMetaData.module_code_id == module_code,
                                         NoteMetaData.date == date).first()
