from googleapiclient import discovery


class BaseGoogleService(object):

    def build(self, http_auth):
        """
        Creates a build function for the API requests. Builds the specific service requests
        Parameters
        ----------
        http_auth: The HttpLib2 object, which contains the current Http request

        Returns
        -------
        A resource object that can be integrated with the API's via requests.
        """
        return discovery.build(self.API, self.VERSION, http=http_auth)

    def execute_request(self, request, http):
        """
        Executes a request to actually interact with the API to perform a request
        Parameters
        ----------
        request
        http: HttpLib2 object of the current Http request

        Returns
        -------
        The result from the API call.
        """
        return request.execute(http=http)