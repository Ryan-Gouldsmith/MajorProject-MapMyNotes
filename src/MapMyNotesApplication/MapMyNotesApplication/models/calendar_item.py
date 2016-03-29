from datetime import datetime
from dateutil import parser


class Calendar_Item(object):

    def __init__(self, item):
        self.item = item

    def format_start_date(self):
        date = self.item["start"]["dateTime"]
        # Had an issue when daylight timings came into play. with datetime, found this http://stackoverflow.com/questions/10494312/parsing-time-string-in-python it was great at informing me about the dateutil
        datetime_item = parser.parse(date)
        #datetime_item = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        return datetime_item.strftime("%d %B %Y %H:%M")
