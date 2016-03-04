from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Module_Code(database.Model):

    __tablename__ = "notes_module_codes"
    id = Column(Integer, primary_key = True)
    module_code = Column(String(50))
    #http://docs.sqlalchemy.org/en/latest/orm/relationships.html
    notes = relationship("Note", backref="module_code")


    def __init__(self, module_code):
        self.module_code = module_code

    def save(self):
        database.session.add(self)
        database.session.commit()
