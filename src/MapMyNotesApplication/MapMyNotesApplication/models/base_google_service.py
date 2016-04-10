from googleapiclient import discovery


class BaseGoogleService(object):

    def build(self, http_auth):
        return discovery.build(self.API, self.VERSION, http=http_auth)

    def execute_request(self, request, http):
        return request.execute(http=http)