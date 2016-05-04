from MapMyNotesApplication import database
from MapMyNotesApplication.models.calendar_item import CalendarItem
from flask import Flask
from flask.ext.testing import TestCase


class TestCalendarItem(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        # http://blog.toast38coza.me/adding-a-database-to-a-flask-app/ Used to help with the test database, maybe could move this to a config file..
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        self.data = {
            "kind": "calendar#event",
            "etag": "\"1234567891012345\"",
            "id": "ideventcalendaritem1",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?testtest",
            "created": "2014-09-10T14:53:25.000Z",
            "updated": "2014-09-10T14:54:12.748Z",
            "summary": "Test Example",
            "creator": {
                "email": "test@gmail.com",
                "displayName": "Tester",
                "self": 'true'
            },
            "organizer": {
                "email": "test@gmail.com",
                "displayName": "Test",
                "self": 'true'
            },
            "start": {
                "dateTime": "2016-12-01T01:00:00Z"
            },
            "end": {
                "dateTime": "2016-12-01T02:30:00Z"
            },
            "transparency": "transparent",
            "visibility": "private",
            "iCalUID": "123456789@google.com",
            "sequence": 0,
            "guestsCanInviteOthers": 'false',
            "guestsCanSeeOtherGuests": 'false',
            "reminders": {
                "useDefault": 'true'
            }
        }
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_creating_a_calendar_item_stores_the_informaiton_correcty(self):
        calendar_item = CalendarItem(self.data)
        assert calendar_item.item == self.data

    def test_formating_a_start_date_returns_the_correct_formatting(self):
        calendar_item = CalendarItem(self.data)
        formatted_date = calendar_item.format_start_date()
        assert "01 December 2016 01:00" in formatted_date
