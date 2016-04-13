from flask import current_app

"""
Although update wasn't used I saw how to make a request to change an event.
Therefore it should be given an honourable reference.
https://developers.google.com/google-apps/calendar/v3/reference/events/update
"""

from MapMyNotesApplication.models.base_google_service import BaseGoogleService


class GoogleCalendarService(BaseGoogleService):
    API = "calendar"
    VERSION = "v3"

    def get_list_of_events(self, service, start=None, end=None):
        print "start {}".format(start)
        if start is not None and end is not None:
            if not self.check_dates_are_correct(start=start, end=end):
                return None

            return service.events().list(calendarId="primary", timeMin=start, timeMax=end, timeZone="Europe/London")

        return service.events().list(calendarId="primary", timeZone="Europe/London")

    def check_dates_are_correct(self, start, end):
        return start < end

    def prepare_url_for_event(self, note):
        return current_app.config['root_url'] + "/show_note/{}".format(note.id)

    def update_event(self, service, event, http_auth):
        google_request = service.events().patch(calendarId='primary', eventId=event['id'], body=event)
        return self.execute_request(google_request, http_auth)

    def remove_note_url_from_description(self, note_url, event, service, http_auth):
        event['description'] = event['description'].replace(note_url, "")
        return self.update_event(service, event, http_auth)

    def add_note_url_to_description(self, note_url, event, service, http_auth):
        if 'description' in event:
            event['description'] += " " + note_url
        else:
            event['descirption'] = note_url
        return self.update_event(service, event, http_auth)

    def get_events_based_on_date(self, start_date, end_date, http_auth, google_service):
        google_request = self.get_list_of_events(google_service, start=start_date, end=end_date)
        google_calendar_response = self.execute_request(google_request, http_auth)
        return google_calendar_response
