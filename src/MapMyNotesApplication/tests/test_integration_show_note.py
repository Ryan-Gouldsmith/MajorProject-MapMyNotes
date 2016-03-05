from MapMyNotesApplication import application, database
from selenium import webdriver
import pytest
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from selenium.webdriver.common.keys import Keys


class TestIntegretationShowNote(LiveServerTestCase):

    def create_app(self):
        app = application
        app.config['LIVESERVER_PORT'] = 5000
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        return app

    def setUp(self):
        # Ideas on how to create the driver and use it. https://realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1024, 640 )

    def tearDown(self):
        self.driver.quit()

    def test_image_loads_on_show_note_page(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        image_src = self.driver.find_element_by_tag_name('img').get_attribute('src')
        url_path = image_src.split("http://localhost:5000")

        assert url_path[1] == "/img/test.png"

    def test_module_code_is_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")
        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        module_code = self.driver.find_element_by_class_name("module_code")

        assert module_code.text == "Module Code: CS31310"

    def test_lectuer_name_is_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")

        assert lecturer_name.text == "By Mr Foo"

    def test_location_name_is_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        location_name = self.driver.find_element_by_class_name("location_name")

        assert location_name.text == "C11 Hugh Owen"
