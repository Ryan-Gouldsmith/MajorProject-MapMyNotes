from flask import current_app

"""
Although update wasn't used I saw how to make a request to change an event.
Therefore it should be given an honourable reference.
https://developers.google.com/google-apps/calendar/v3/reference/events/update
As well as:
https://developers.google.com/google-apps/calendar/v3/
"""

from MapMyNotesApplication.models.base_google_service import BaseGoogleService


class GoogleCalendarService(BaseGoogleService):
    # CONSTANTS
    API = "calendar"
    VERSION = "v3"

    def get_list_of_events(self, service, start=None, end=None):
        """
        Creates the query to return a list of events from the calendar
        Parameters
        ----------
        service: The Google service object request: I.e google calendar
        start: String The start date for the events
        end: String the end date for the event

        Returns
        -------
        A list of events either between a selection of dates or the full list
        """
        if start is not None and end is not None:
            if not self.check_dates_are_correct(start=start, end=end):
                return None
            return service.events().list(calendarId="primary", timeMin=start, timeMax=end, timeZone="Europe/London")

        return service.events().list(calendarId="primary", timeZone="Europe/London")

    def check_dates_are_correct(self, start, end):
        """
        Checks that the dates are the correct way around
        Parameters
        ----------
        start: the start date
        end: The end date

        Returns
        -------
        True if the dates are valid
        False if the dates are not valid
        """
        return start < end

    def prepare_url_for_event(self, note):
        """
        Creates the string representation for saving to a calendar event
        Parameters
        ----------
        note: The note which is currently been saved

        Returns
        -------
        String representation of the show note route

        """
        return current_app.config['root_url'] + "/show_note/{}".format(note.id)

    def update_event(self, service, event, http_auth):
        """
        Uses the HTTP Patch method to update a calendar event item with a body
        Parameters
        ----------
        service: The google calendar service in question
        event: JSON - The event which is being updated
        http_auth: Httplib2 object for the current request

        Returns
        -------
        A JSON representation of the updated event.
        """
        google_request = service.events().patch(calendarId='primary', eventId=event['id'], body=event)
        return self.execute_request(google_request, http_auth)

    def remove_note_url_from_description(self, note_url, event, service, http_auth):
        """
        Removes a string representation of the note from a given event
        Parameters
        ----------
        note_url: String - The url which is being replaced
        event: Dict - The event being updated
        service: The Google calendar Service
        http_auth: HTTPLib2 object for querying the API

        Returns
        -------
        A JSON representation of the updated event minus the URL
        """
        event['description'] = event['description'].replace(note_url, "")
        return self.update_event(service, event, http_auth)

    def add_note_url_to_description(self, note_url, event, service, http_auth):
        """
        Appends a note's url to the user's calendar item
        Parameters
        ----------
        note_url: String - representation of the note url
        event: Dict - The event being updated
        service: The Google Calendar service being used to query the API
        http_auth: HTTPLib2 object which is used to complete the request

        Returns
        -------
        An updated dict event from the service with the url in the description
        """
        if 'description' in event:
            event['description'] += " " + note_url
        else:
            event['description'] = note_url
        return self.update_event(service, event, http_auth)

    def get_events_based_on_date(self, start_date, end_date, http_auth, google_service):
        """
        Gets a series of events from the Google Calendar API based on the date entered
        Parameters
        ----------
        start_date: String - The start date for the when the events should start from
        end_date: String - The end date for when the events should end
        http_auth: HttpLib2 object for the request
        google_service: Google service to interact with the API

        Returns
        -------

        """
        google_request = self.get_list_of_events(google_service, start=start_date, end=end_date)
        google_calendar_response = self.execute_request(google_request, http_auth)
        return google_calendar_response

    def get_recurring_event_list(self, start, end, event_id, http_auth, google_service):
        """
        Get all the reoccurring events based on a given reoccurring event ID.
        Parameters
        ----------
        start: String - Start date for the event
        end: String - End date for the event
        event_id: Dict - event ID which is the one being reoccurred.
        http_auth: HttpLib2 object for querying
        google_service: Google services requested to complete the API request

        Returns
        -------
        The list of reoccuring event items as JSON.
        """
        request = google_service.events().instances(calendarId="primary", eventId=event_id, timeMin=start, timeMax=end)
        return self.execute_request(request, http_auth)
