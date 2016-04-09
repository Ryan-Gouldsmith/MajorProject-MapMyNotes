from apiclient import discovery

"""
 Excellent API's from : https://developers.google.com/+/web/api/rest/latest/people/get#examples
"""


class GooglePlusService(object):
    API = "plus"
    VERSION = "v1"

    def build(self, http):
        return discovery.build(self.API, self.VERSION, http=http)

    def get_request_user_authorised(self, service):
        return service.people().get(userId='me')

    def execute(self, request, http):
        return request.execute(http=http)

    def parse_response_for_email(self, response):
        return response["emails"][0]['value']
