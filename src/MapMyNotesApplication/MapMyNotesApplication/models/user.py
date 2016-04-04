from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String, ForeignKey


class User(database.Model):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(100), nullable=False)

    def __init__(self, email_address):
        self.email_address = email_address

    def save(self):
        if len(self.email_address) > 100:
            return False
        database.session.add(self)
        database.session.commit()
