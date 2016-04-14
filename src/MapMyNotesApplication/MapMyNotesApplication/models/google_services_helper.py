import httplib2

from MapMyNotesApplication.models.date_time_helper import DateTimeHelper
from MapMyNotesApplication.models.oauth_service import OauthService


class GoogleServicesHelper(object):
    @staticmethod
    def authorise(session_helper):
        service = OauthService()
        session_credentials = session_helper.return_session_credentials()
        http_auth = service.authorise(httplib2.Http(), session_credentials)
        credentials = service.get_credentials()
        return credentials, http_auth

    @staticmethod
    def get_event_containing_module_code(module_code, calendar_response, start_date):
        # some events come back like 2016-02-16T10:30:00Z other's come back like 2016-02-16T10:30:00+00:00
        start_date = start_date.replace(tzinfo=None).isoformat("T")
        for event in calendar_response["items"]:
            if event['status'] != 'cancelled' and module_code in event['summary'].upper() and start_date in \
                    event['start']['dateTime']:
                return event
        return None

    @staticmethod
    def get_events_based_on_date_time(date_time, google_calendar_service, google_service, http_auth):
        date_time_helper = DateTimeHelper(combined_date_time=date_time)
        start_date, end_date = date_time_helper.process_time_zone()
        google_calendar_response = google_calendar_service.get_events_based_on_date(start_date, end_date, http_auth,
                                                                                    google_service)
        return google_calendar_response

    @staticmethod
    def get_reoccurring_events_based_on_datetime(date_time, google_calendar_service, google_service, http_auth,
                                                 response_original):
        date_time_helper = DateTimeHelper(combined_date_time=date_time)
        start_date, end_date = date_time_helper.process_time_zone()
        reoccurring_events = {}
        reoccurring_events['items'] = []
        for event in response_original['items']:
            if 'recurrence' in event:
                event_id = event['id']
                new_response = google_calendar_service.get_recurring_event_list(start_date, end_date, event_id,
                                                                                http_auth,
                                                                                google_service)
                [reoccurring_events['items'].append(response) for response in new_response['items']]

        return reoccurring_events['items']
