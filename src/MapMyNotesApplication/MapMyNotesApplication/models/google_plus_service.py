from apiclient import discovery

"""
 Excellent API's from : https://developers.google.com/+/web/api/rest/latest/people/get#examples
"""
from MapMyNotesApplication.models.base_google_service import BaseGoogleService


class GooglePlusService(BaseGoogleService):
    #CONSTANTS
    API = "plus"
    VERSION = "v1"

    def get_request_user_authorised(self, service):
        """
        Create the request to get the User's information
        Parameters
        ----------
        service: The Google Plus service

        Returns
        -------
        A service object ready to perform some querying with.
        """
        return service.people().get(userId='me')

    def parse_response_for_email(self, response):
        """
        Parses the email from the JSON response
        Parameters
        ----------
        response: The JSON response from the executed request.

        Returns
        -------
        The email address for the user currently logged in.

        """
        return response["emails"][0]['value']
