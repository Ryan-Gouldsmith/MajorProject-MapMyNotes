from MapMyNotesApplication import application, database
import pytest
import os
from flask import request
from flask.ext.testing import TestCase


class TestOAuthRoute(TestCase):

    def create_app(self):
        app = application
        app.config['TESTING'] = True
        return app

    def test_call_back_route_returns_a_success_status(self):
        response = self.client.get("/oauthsubmit")
        url_full = response.headers.get("Location")

        url_path = url_full

        assert "accounts.google.com" in url_path
        assert response.status_code == 302
