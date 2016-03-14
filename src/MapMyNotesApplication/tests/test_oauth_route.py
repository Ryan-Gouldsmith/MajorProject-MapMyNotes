from MapMyNotesApplication import application, database
import pytest
import os
from flask import request

class TestOAuthRoute(object):

    def setup(self):
        self.app = application.test_client()

    def test_call_back_route_returns_a_success_status(self):
        response = self.app.get("/oauthsubmit")
        url_full = response.headers.get("Location")

        url_path = url_full

        assert "accounts.google.com" in url_path
        assert response.status_code == 302
