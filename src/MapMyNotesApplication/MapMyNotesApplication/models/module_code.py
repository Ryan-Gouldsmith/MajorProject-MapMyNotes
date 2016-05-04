from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

"""
Extends the SQLAlchemy default Model
"""
class ModuleCode(database.Model):
    __tablename__ = "notes_module_codes"
    id = Column(Integer, primary_key=True)
    module_code = Column(String(50), nullable=False)
    # http://docs.sqlalchemy.org/en/latest/orm/relationships.html
    meta_data = relationship("NoteMetaData", backref="module_code")

    def __init__(self, module_code):
        """
        Creates a module instance based on module code
        Parameters
        ----------
        module_code: String representation of the module code
        """
        self.module_code = module_code

    def save(self):
        """
        Save the current instance to the database
        Returns
        -------
        False is there is an error with the length of the modulecode
        """
        if len(self.module_code) > 50:
            return False
        database.session.add(self)
        database.session.commit()

    @staticmethod
    def find_id_by_module_code(module_code):
        """
        Static method for finding an instance of the module code based on the module code
        Parameters
        ----------
        module_code: The module code instance that is being attempted to be found

        Returns
        -------
        A ModuleCode if it exists or None if it does not.
        """
        prepared_module_code = "%{0}%".format(module_code)
        # http://docs.sqlalchemy.org/en/latest/orm/query.html
        query = ModuleCode.module_code.like(prepared_module_code)
        return ModuleCode.query.filter(query).first()
