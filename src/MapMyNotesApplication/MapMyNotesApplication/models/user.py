from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String

"""
Interacts with the SQLAlchemy model
"""
class User(database.Model):
    #SQL Alchemy model specific attributes
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(100), nullable=False)

    def __init__(self, email_address):
        """
        Creates a new instance of the user
        Parameters
        ----------
        email_address: String representation of the user
        """
        self.email_address = email_address

    def save(self):
        """
        Saves the current instance to the database
        Returns
        -------
        False if there is an error.
        """
        if len(self.email_address) > 100:
            return False
        database.session.add(self)
        database.session.commit()

    @staticmethod
    def find_user_by_email_address(email_address):
        """
        Uses the SQLAlchemy API's to extract the email address from the database
        Parameters
        ----------
        email_address: String representation of the email address that's been attempted to be discovered

        Returns
        -------
        An instance of User if email address has been found
        None if there has been no results found.
        """
        return User.query.filter_by(email_address=email_address).one_or_none()
