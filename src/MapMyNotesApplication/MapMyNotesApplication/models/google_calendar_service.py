from apiclient import discovery
from flask import current_app

"""
Although update wasn't used I saw how to make a request to change an event.
Therefore it should be given an honourable reference.
https://developers.google.com/google-apps/calendar/v3/reference/events/update
"""


class GoogleCalendarService(object):
    API = "calendar"
    VERSION = "v3"

    def build(self, http_auth):
        return discovery.build(self.API, self.VERSION, http=http_auth)

    def get_list_of_events(self, service, start=None, end=None):

        if start is not None and end is not None:
            if self.check_dates_are_correct(start=start, end=end) is False:
                return None

            return service.events().list(calendarId="primary", timeMin=start, timeMax=end, timeZone="Europe/London")

        return service.events().list(calendarId="primary", timeZone="Europe/London")

    def execute_request(self, request, http):
        return request.execute(http=http)

    def check_dates_are_correct(self, start, end):
        return start < end

    def prepare_url_for_event(self, note):
        return current_app.config['root_url'] + "/show_note/{}".format(note.id)

    def add_url_to_event_description(self, service, note_url, event):
        event["description"] = note_url
        return service.events().patch(calendarId='primary', eventId=event['id'], body=event)
