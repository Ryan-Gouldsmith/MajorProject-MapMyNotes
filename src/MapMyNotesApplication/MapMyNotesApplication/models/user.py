from MapMyNotesApplication import database
from sqlalchemy import Column, Integer, String


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

    @staticmethod
    def find_user_by_email_address(email_address):
        return User.query.filter_by(email_address=email_address).one_or_none()
