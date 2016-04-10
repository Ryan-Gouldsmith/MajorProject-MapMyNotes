from datetime import datetime, time

from flask import Flask
from flask.ext.testing import TestCase

from MapMyNotesApplication import database
from MapMyNotesApplication.models.date_time_helper import DateTimeHelper


class TestDateTimeHelper(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        """
         http://blog.toast38coza.me/adding-a-database-to-a-flask-app/
         Used to help with the test database, could move this to a config file.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        app.config['SECRET_KEY'] = "secret"
        return app

    def setUp(self):
        database.session.close()
        database.drop_all()
        database.create_all()

    def test_is_date_formatted_correctly_should_return_true_for_valid_date(self):
        date_time_helper = DateTimeHelper("20 March 2016")
        formatted_correctly = date_time_helper.is_date_formatted_correctly()

        assert formatted_correctly is True

    def test_is_date_formatted_correctly_should_return_false_for_invalid_date(self):
        date_time_helper = DateTimeHelper("20 2016")
        formatted_correctly = date_time_helper.is_date_formatted_correctly()

        assert formatted_correctly is False

    def test_is_time_formatted_correctly_returns_true_for_valid_times(self):
        date_time_helper = DateTimeHelper(time="20:30")
        formatted_correctly = date_time_helper.is_time_formatted_correctly()

        assert formatted_correctly is True

    def test_is_time_formatted_correctly_returns_false_for_invalid_times(self):
        date_time_helper = DateTimeHelper(time="2900:30")
        formatted_correctly = date_time_helper.is_time_formatted_correctly()

        assert formatted_correctly is False

    def test_setting_the_date_correctly_sets_attribute(self):
        date_time_helper = DateTimeHelper()
        date_time_helper.set_date("20 March 2016")

        assert date_time_helper.raw_date == "20 March 2016"

    def test_setting_the_time_correctly_sets_attribute(self):
        date_time_helper = DateTimeHelper()
        date_time_helper.set_time("14:00")

        assert date_time_helper.raw_time == "14:00"

    def test_converting_string_date_and_time_to_datetime_returns_datetime_object(self):
        date_time_helper = DateTimeHelper('20 March 2016', "20:00")
        date_time_object = date_time_helper.convert_string_date_and_time_to_datetime()

        assert type(date_time_object) is datetime
        assert date_time_object == datetime(2016, 3, 20, 20, 0)

    def test_process_time_zone_returns_the_correct_start_and_end_date(self):
        date_time_helper = DateTimeHelper('20 March 2016', "20:00")
        _ = date_time_helper.convert_string_date_and_time_to_datetime()
        start, end = date_time_helper.process_time_zone()
        expected_start = "2016-03-20T20:00"
        expected_end = '2016-03-20T23:59:00'
        assert expected_start in start
        assert expected_end in end

    def test_return_time_object_returns_the_correct_time(self):
        date_time_helper = DateTimeHelper('20 March 2016', "20:00")
        time_object = date_time_helper.return_time_object("20:00")

        assert time(20, 0) == time_object

    def test_combine_date_and_time_returns_correct_date_time(self):
        date_time_helper = DateTimeHelper('20 March 2016', "20:00")
        suggested_date = datetime.strptime("20 March 2016", "%d %B %Y")
        suggested_time = datetime.strptime("10:10", "%H:%M")

        combined = date_time_helper.combine_date_and_time(suggested_date.date(), suggested_time.time())

        assert combined == datetime(2016, 3, 20, 10, 10)

    def test_process_suggested_date_for_calendar_events_should_return_correct_suggested_date(self):
        date_time_helper = DateTimeHelper('20 March 2016', "20:00")
        suggested_date, end_date, start_date = date_time_helper.process_suggested_date_for_calendar_events(
            "2017:04:04 14:14:14")

        assert suggested_date == datetime(2017, 4, 4, 14, 14, 14)
        assert end_date == '2017-04-04T23:59:00Z'
        assert start_date == '2017-04-04T00:00:00Z'

    def test_get_last_7_days_of_dates_returns_both_end_and_start_date(selfs):
        end, start = DateTimeHelper.get_last_7_days_of_dates()

        assert type(end) is not None
        assert type(start) is not None

    def test_convert_date_time_to_string_representation_returns_correct_string_representation(self):
        string_representation = DateTimeHelper.convert_date_time_to_string_representation(datetime(2016, 3, 20, 20, 0))
        assert string_representation == "20 March 2016 20:00"

    def test_convert_datetime_to_string_date_and_time_returns_both_a_date_and_time_object(self):
        time_parsed, date_parsed = DateTimeHelper.convert_datetime_to_string_date_and_time(datetime(2016, 3, 20, 20, 0))
        assert time_parsed == '20:00'
        assert date_parsed == "20 March 2016"
