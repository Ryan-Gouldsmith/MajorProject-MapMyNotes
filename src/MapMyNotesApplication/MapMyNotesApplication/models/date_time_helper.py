from datetime import datetime, timedelta

from dateutil import tz


class DateTimeHelper(object):
    DEFAULT_TIME_ZONE = 'Europe/London'
    HOUR_PATTERN_MATCH = "%H:%M"
    DATE_PATTERN_MATCH = "%d %B %Y"
    MAX_HOUR = "23:59"
    MIN_HOUR = "0:00"
    TIME_SYMBOL = "T"
    TIME_ZONE_SYMBOL = "Z"
    FULL_DATE_TIME_STRING_PATTERN_MATCH = "%d %B %Y %H:%M"
    EVENT_DATE_TIME_FORMAT = "%Y:%m:%d %H:%M:%S"

    def __init__(self, date=None, time=None, combined_date_time=None):
        self.raw_date = date
        self.raw_time = time
        self.date_time_date_object = None
        self.date_time_time_object = None
        self.combined_date_time_object = combined_date_time

    """
    REFERENCE:
    http://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    No build in function so I needed to see how I could catch the ValueError
    """

    def is_date_formatted_correctly(self):
        try:
            datetime.strptime(self.raw_date, self.DATE_PATTERN_MATCH)
            return True
        except ValueError:
            return False

    def is_time_formatted_correctly(self):
        try:
            datetime.strptime(self.raw_time, self.HOUR_PATTERN_MATCH)
            return True
        except ValueError:
            return False

    def set_date(self, date):
        self.raw_date = date

    def set_time(self, time):
        self.raw_time = time

    def convert_string_date_and_time_to_datetime(self):
        self.date_time_date_object = datetime.strptime(self.raw_date, self.DATE_PATTERN_MATCH)
        self.date_time_time_object = datetime.strptime(self.raw_time, self.HOUR_PATTERN_MATCH)
        self.combined_date_time_object = self.combine_date_and_time(self.date_time_date_object.date(),
                                                                    self.date_time_time_object.time())
        return self.combined_date_time_object

    @staticmethod
    def convert_datetime_to_string_date_and_time(date_time):
        time = date_time.strftime(DateTimeHelper.HOUR_PATTERN_MATCH)
        date = date_time.strftime(DateTimeHelper.DATE_PATTERN_MATCH)
        return time, date

    @staticmethod
    def convert_date_time_to_string_representation(date_time):
        return date_time.strftime(DateTimeHelper.FULL_DATE_TIME_STRING_PATTERN_MATCH)

    def process_time_zone(self):
        """ Great API
        https://docs.python.org/2/library/datetime.html#datetime.datetime.replace
        Had issue with the BST. Had to supply the timezone offset to Google API.
        """
        date_time = self.combined_date_time_object.replace(tzinfo=tz.gettz(self.DEFAULT_TIME_ZONE))
        start_date = date_time.isoformat(self.TIME_SYMBOL)

        end_time = self.return_time_object(self.MAX_HOUR)
        end_date = self.combine_date_and_time(date_time.date(), end_time)

        end_date = end_date.replace(tzinfo=tz.gettz(self.DEFAULT_TIME_ZONE))
        end_date = end_date.isoformat(self.TIME_SYMBOL)

        return start_date, end_date

    def return_time_object(self, time_value):
        return datetime.strptime(time_value, self.HOUR_PATTERN_MATCH).time()

    def combine_date_and_time(self, date, time):
        return datetime.combine(date, time)

    def process_suggested_date_for_calendar_events(self, suggested_date):
        suggested_date = datetime.strptime(suggested_date, self.EVENT_DATE_TIME_FORMAT)

        end_time = self.return_time_object(self.MAX_HOUR)
        start_time = self.return_time_object(self.MIN_HOUR)

        end_date = self.combine_date_and_time(suggested_date.date(), end_time).isoformat(
            self.TIME_SYMBOL) + self.TIME_ZONE_SYMBOL
        start_date = self.combine_date_and_time(suggested_date.date(), start_time).isoformat(
            self.TIME_SYMBOL) + self.TIME_ZONE_SYMBOL

        return suggested_date, end_date, start_date

    @staticmethod
    def get_last_7_days_of_dates():
        end_date = datetime.utcnow().isoformat(DateTimeHelper.TIME_SYMBOL) + DateTimeHelper.TIME_ZONE_SYMBOL
        start_date = (datetime.utcnow() - timedelta(days=7)).isoformat(
            DateTimeHelper.TIME_SYMBOL) + DateTimeHelper.TIME_ZONE_SYMBOL
        return end_date, start_date
