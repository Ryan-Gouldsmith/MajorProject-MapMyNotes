from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Module_Code(database.Model):

    __tablename__ = "notes_module_codes"
    id = Column(Integer, primary_key=True)
    module_code = Column(String(50), nullable=False)
    # http://docs.sqlalchemy.org/en/latest/orm/relationships.html
    meta_data = relationship("Note_Meta_Data", backref="module_code")

    def __init__(self, module_code):
        self.module_code = module_code

    def save(self):
        if len(self.module_code) > 50:
            return False
        database.session.add(self)
        database.session.commit()

    @staticmethod
    def find_id_by_module_code(filename):
        prepared_file = "%{0}%".format(filename)
        # http://docs.sqlalchemy.org/en/latest/orm/query.html
        query = Module_Code.module_code.like(prepared_file)
        return Module_Code.query.filter(query).first()
