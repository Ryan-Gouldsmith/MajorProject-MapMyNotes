from datetime import datetime
class Calendar_Item(object):

    def __init__(self, item):
        self.item = item

    def format_start_date(self):
        date = self.item["start"]["dateTime"]
        datetime_item = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        return datetime_item.strftime("%d %B %Y %H:%M")
