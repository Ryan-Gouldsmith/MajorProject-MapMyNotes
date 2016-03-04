from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask
from flask.ext.testing import LiveServerTestCase

class TestIntegrationHomepage(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        return app

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()


    def test_should_display_correct_homepage_title(self):
        print self.get_server_url()
        self.driver.get(self.get_server_url())
        title = self.driver.find_element_by_tag_name('h1')
        assert "Welcome to the home page" == title.text
