from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String, ForeignKey
from MapMyNotesApplication.models.module_code import Module_Code

class Note(database.Model):

    __tablename__ = "notes"
    id = Column(Integer, primary_key = True)
    image_path = Column(String(150))
    module_code_id = Column(Integer, ForeignKey(Module_Code.id))


    def __init__(self, path, module_code):
        self.image_path = path
        self.module_code_id = module_code

    def save(self):
        database.session.add(self)
        database.session.commit()
