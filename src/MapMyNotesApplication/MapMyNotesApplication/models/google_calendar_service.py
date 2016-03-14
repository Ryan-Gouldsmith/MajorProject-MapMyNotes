import os
from oauth2client import client
from apiclient import discovery


class Google_Calendar_Service(object):

    API = "calendar"
    VERSION = "v3"

    def build(self,http):
        return discovery.build(self.API, self.VERSION, http=http)
