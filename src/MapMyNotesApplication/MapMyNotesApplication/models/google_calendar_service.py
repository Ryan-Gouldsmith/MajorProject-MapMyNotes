import os
from oauth2client import client
from apiclient import discovery


class Google_Calendar_Service(object):

    API = "calendar"
    VERSION = "v3"

    def build(self,http_auth):
        return discovery.build(self.API, self.VERSION, http=http_auth)

    def get_list_of_events(self, service, start=None, end=None):

        if start is not None and end is not None:
            if self.check_dates_are_correct(start=start, end=end) is False:
                return None

            return service.events().list(calendarId="primary", timeMin=start, timeMax=end)

        return service.events().list(calendarId="primary")

    def execute_request(self, request, http):
        return request.execute(http=http)

    def check_dates_are_correct(self, start, end):
        return start < end
