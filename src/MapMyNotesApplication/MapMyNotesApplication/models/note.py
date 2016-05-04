from MapMyNotesApplication import database
from MapMyNotesApplication.models.module_code import ModuleCode
from MapMyNotesApplication.models.note_meta_data import NoteMetaData
from MapMyNotesApplication.models.user import User
from sqlalchemy import Column, Integer, String, ForeignKey, and_

"""
Extends SQLAlchemy model
"""
class Note(database.Model):
    __tablename__ = "notes"
    #SQL ALCHEMY declarations
    id = Column(Integer, primary_key=True)
    image_path = Column(String(150), nullable=False)
    note_meta_data_id = Column(Integer, ForeignKey(NoteMetaData.id))
    calendar_url = Column(String(256))
    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, path, meta_data_id, user_id):
        """
        Creates a new instance of a note
        Parameters
        ----------
        path: String - to the path of the image
        meta_data_id: Int - metadata ID.
        user_id: Int - the user's id
        """
        self.image_path = path
        self.note_meta_data_id = meta_data_id
        self.user_id = user_id

    def save(self):
        """
        Saves a specific instance to the relation
        Returns
        -------
        False if there was an error saving the instance
        """
        if len(self.image_path) > 150:
            return False
        if self.calendar_url is not None and len(self.calendar_url) > 256:
            return False
        database.session.add(self)
        database.session.commit()

    def delete(self):
        """
        Removes the current instance from the database
        """
        database.session.delete(self)
        database.session.commit()

    def update_meta_data_id(self, meta_data_id):
        """
        Updates the foreign key id with a new meta data ID, then saves the object
        Parameters
        ----------
        meta_data_id: The new metadata ID that is being attached to a note
        """
        """
        http://stackoverflow.com/questions/9667138/how-to-update-sqlalchemy-row-entry
        """
        self.note_meta_data_id = meta_data_id
        self.save()

    def update_calendar_url(self, calendar_url):
        """
        Updates the string representation of the calendar URL attribute
        Parameters
        ----------
        calendar_url: String - Calendar URL which is going to update the current attribute
        """
        self.calendar_url = calendar_url
        self.save()

    @staticmethod
    def find_note_by_module_code(module_code, user_id):
        """
        Finds a specific note from the module code. Has to join the note meta data table and the module code by the
        Relationship which has been defined.

        Parameters
        ----------
        module_code: String - The module code attempted to be found
        user_id: Int - The ID of the current user

        Returns
        -------
        An Array of Notes which match a given ID.
        """
        # API REFERENCE : http://docs.sqlalchemy.org/en/rel_1_0/orm/query.html#sqlalchemy.orm.query.Query.join
        query = ModuleCode.module_code.like(module_code)
        return Note.query.join(NoteMetaData.meta_data).join(NoteMetaData.module_code).filter(
            and_(Note.user_id == user_id, query)).all()
