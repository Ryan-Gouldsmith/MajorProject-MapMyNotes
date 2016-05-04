from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from MapMyNotesApplication import database
from MapMyNotesApplication.models.module_code import ModuleCode

"""
Extends SQLAlchemy Model
"""


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
        """
        Creates a new instance of the note meta-data
        Parameters
        ----------
        lecturer_name: String - the lecturer from the form
        module_code: String - The module code from the form
        location: String - The location from the form
        date: DateTime - A combined object from the date and time from the form
        title: String - A title from the form.
        """
        self.lecturer = lecturer_name
        self.module_code_id = module_code
        self.location = location
        self.date = date
        self.title = title

    def save(self):
        """
        Save the current instance of the NoteMetaData to the relation
        Returns
        -------
        False if there was an error
        True if everything worked.
        """
        if len(self.lecturer) > 100 or len(self.location) > 100 or len(self.title) > 100:
            return False

        database.session.add(self)
        database.session.commit()
        return True

    def update_module_code_id(self, module_code_id):
        """
        Updates this specific instance of the module code id with a new value
        Parameters
        ----------
        module_code_id: Int - new module code id instance
        """
        self.module_code_id = module_code_id
        self.save()

    @staticmethod
    def find_meta_data(meta_data):
        """
        Static method for finding an already existing NoteMetaData. Compares all the attributes to see if they match.
        Parameters
        ----------
        meta_data: An Object of some meta-data to attempt to find it.

        Returns
        -------
        An instance of One NoteMetaData relation.

        """
        lecturer = meta_data.lecturer
        location = meta_data.location
        module_code = meta_data.module_code_id
        date = meta_data.date

        return NoteMetaData.query.filter(NoteMetaData.lecturer == lecturer, NoteMetaData.location == location,
                                         NoteMetaData.module_code_id == module_code,
                                         NoteMetaData.date == date).first()
