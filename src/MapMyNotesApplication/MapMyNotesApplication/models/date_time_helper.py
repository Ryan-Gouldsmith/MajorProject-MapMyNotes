from datetime import datetime, timedelta

from dateutil import tz


class DateTimeHelper(object):
    """ CONSTANTS"""
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
        """
        Initialised a new date helper
        Parameters
        ----------
        date: The string representation of the date
        time: The string representation of the time
        combined_date_time: The combined datetime object
        """
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
        """
        Checks to see if the date is formatted correctly again the DATE PATTERN MATCH variable
        Returns
        -------
        True is the date is formatted correctly.
        False if the date is not formatted correctly.
        """
        try:
            datetime.strptime(self.raw_date, self.DATE_PATTERN_MATCH)
            return True
        except ValueError:
            return False

    def is_time_formatted_correctly(self):
        """
        Checks to see if the time is formatted correctly against the hour pattern match
        Returns
        -------
        True if the time is formatted correctly.
        False if the time is not formatted correctly.
        """
        try:
            datetime.strptime(self.raw_time, self.HOUR_PATTERN_MATCH)
            return True
        except ValueError:
            return False

    def set_date(self, date):
        """
        Sets a string representation of the date
        Parameters
        ----------
        date: String representation of the date.
        """
        self.raw_date = date

    def set_time(self, time):
        """
        Sets the string representation of the time
        Parameters
        ----------
        time: String representation of the time
        """
        self.raw_time = time

    def convert_string_date_and_time_to_datetime(self):
        """
        Converts the string representation of the date and time into a datetime object
        Returns
        -------
        A DateTime object which is represented by the strings.
        """
        self.date_time_date_object = datetime.strptime(self.raw_date, self.DATE_PATTERN_MATCH)
        self.date_time_time_object = datetime.strptime(self.raw_time, self.HOUR_PATTERN_MATCH)
        self.combined_date_time_object = self.combine_date_and_time(self.date_time_date_object.date(),
                                                                    self.date_time_time_object.time())
        return self.combined_date_time_object

    @staticmethod
    def convert_datetime_to_string_date_and_time(date_time):
        """
        STATIC method for converting a datetime to a string.
        Parameters
        ----------
        date_time: DateTime Object that needs to be converted

        Returns
        -------
        Time: String representation of the datetime object
        Date: String representation of the date object.
        """
        time = date_time.strftime(DateTimeHelper.HOUR_PATTERN_MATCH)
        date = date_time.strftime(DateTimeHelper.DATE_PATTERN_MATCH)
        return time, date

    @staticmethod
    def convert_date_time_to_string_representation(date_time):
        """
        Converts a date time into a string using the DATE TIME STRING PATTERN MATCH attribute
        Parameters
        ----------
        date_time: DateTime object needed to convert it to a string

        Returns
        -------
        String representation of the date time in the format of "%d %B %Y %H:%M"
        """
        return date_time.strftime(DateTimeHelper.FULL_DATE_TIME_STRING_PATTERN_MATCH)

    def process_time_zone(self):
        """
        Processes the timezone of the combined date time object so that it appends it to the end
        Returns
        -------
        Start date: The String representation of the start date
        End date: The string representation of the end date.
        """
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
        """
        Creates a time object from the string time value
        Parameters
        ----------
        time_value: String representation of the time

        Returns
        -------
        Time object which matches the HOUR PATTERN.
        """
        return datetime.strptime(time_value, self.HOUR_PATTERN_MATCH).time()

    def combine_date_and_time(self, date, time):
        """
        Combines both a date object and a time object to return a DateTime object
        Parameters
        ----------
        date: DateObject which needs to be combined
        time: TimeObject which needs to be combined

        Returns
        -------
        A DateTime object.
        """
        return datetime.combine(date, time)

    def process_suggested_date_for_calendar_events(self, suggested_date):
        """
        From a string date then it will create a datetime object which creates specific time objects up to 23:59 hours
        Parameters
        ----------
        suggested_date: The string representation of the date needing to be parsed

        Returns
        -------
        Suggested Date: String representation of the suggested date
        End_date: Date Object with the date collected from the suggested date, the last hour in that day.
        Start_date: The start date time which was passed in.
        """
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
        """
        STATIC method. Gets the last 7 days from the date time function
        Returns
        -------
        end_date: The end DateTime sting for the 7 days.
        start_date: The date -7 days from the current date.
        """

        # https://docs.python.org/2/library/datetime.html#datetime.datetime.utcnow Gets the current time as native
        # Datetime object
        end_date = datetime.utcnow().isoformat(DateTimeHelper.TIME_SYMBOL) + DateTimeHelper.TIME_ZONE_SYMBOL
        # Helped with the subtract that I wanted to achieve:
        # http://stackoverflow.com/questions/441147/how-can-i-subtract-a-day-from-a-python-date
        start_date = (datetime.utcnow() - timedelta(days=7)).isoformat(
            DateTimeHelper.TIME_SYMBOL) + DateTimeHelper.TIME_ZONE_SYMBOL
        return end_date, start_date
