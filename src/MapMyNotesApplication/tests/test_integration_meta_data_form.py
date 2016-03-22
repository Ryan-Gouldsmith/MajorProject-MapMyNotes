from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask
from flask.ext.testing import LiveServerTestCase


#https://books.google.co.uk/books?id=Xd0DCgAAQBAJ&pg=PA77&lpg=PA77&dq=flask-testing+liveservertestcase+selenium&source=bl&ots=fhCVat8wgm&sig=2ehfPK93v8fS2NQEq_vzdKYbc-U&hl=en&sa=X&ved=0ahUKEwiCr7ns6KLLAhVCUhQKHVO0DWoQ6AEIPTAF#v=onepage&q=flask-testing%20liveservertestcase%20selenium&f=false Docs are terrible this book may be good.
class TestIntegrationMetaDataForm(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'

        return app

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )

    def tearDown(self):
        self.driver.quit()


    def test_form_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        form = self.driver.find_element_by_tag_name('form')
        assert form.is_displayed() is True

    def test_submit_button_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        submit_button = self.driver.find_element_by_class_name("submit")
        assert submit_button.is_displayed() is True

    def test_module_field_label_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        module_label = self.driver.find_element_by_class_name("module_label")
        assert module_label.is_displayed() is True

    def test_module_field_label_content(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        module_label_content = self.driver.find_element_by_class_name("module_label")
        assert module_label_content.text == "Module Code:"

    def test_form_has_module_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        module_field = self.driver.find_element_by_class_name("module_code_data")
        assert module_field.is_displayed() is True

    def test_form_has_correct_url_action(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        form_action = self.driver.find_element_by_tag_name("form").get_attribute("action")

        path = form_action.split("http://localhost:5000")

        expected_url = "/metadata/add/test.png"

        assert expected_url == path[1]

    def test_form_has_lecturer_name_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        lecturer_field = self.driver.find_element_by_class_name("lecturer_name")
        assert lecturer_field.is_displayed() is True

    def test_form_has_location_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        location_field = self.driver.find_element_by_class_name("location_name")

        assert location_field.is_displayed() is True

    def test_form_has_date_of_lecturer_field(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        date_field = self.driver.find_element_by_class_name("date")

        assert date_field.is_displayed() is True

    def test_form_has_title_exists(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        title_field = self.driver.find_element_by_class_name('title')
        assert title_field.is_displayed() is True
