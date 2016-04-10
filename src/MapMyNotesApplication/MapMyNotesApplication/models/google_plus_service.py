from apiclient import discovery

"""
 Excellent API's from : https://developers.google.com/+/web/api/rest/latest/people/get#examples
"""
from MapMyNotesApplication.models.base_google_service import BaseGoogleService


class GooglePlusService(BaseGoogleService):
    API = "plus"
    VERSION = "v1"

    def get_request_user_authorised(self, service):
        return service.people().get(userId='me')

    def parse_response_for_email(self, response):
        return response["emails"][0]['value']
