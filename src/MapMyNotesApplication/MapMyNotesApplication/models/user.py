from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String, ForeignKey


class User(database.Model):

    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    email_address = Column(String(100))

    def __init__(self, email_address):
        self.email_address = email_address

    def save(self):
        database.session.add(self)
        database.session.commit()
