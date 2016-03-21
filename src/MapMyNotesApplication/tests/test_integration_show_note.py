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
        database.session.close()
        database.drop_all()
        database.create_all()


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

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12th February 2016 16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

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

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12th February 2016 16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

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

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12th February 2016 16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

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

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12th February 2016 16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        location_name = self.driver.find_element_by_class_name("location_name")

        assert location_name.text == "C11 Hugh Owen"

    def test_date_values_are_correct(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12th February 2016 16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        date_value = self.driver.find_element_by_class_name("date")

        assert date_value.text == "12th February 2016 16:00"

    def test_delete_link_is_available(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12th February 2016 16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        delete_link = self.driver.find_element_by_class_name('delete_note')

        delete_form = self.driver.find_element_by_class_name('delete_note_form').get_attribute("action").split("http://localhost:5000")

        assert delete_link.is_displayed() is True

        assert delete_form[1] == "/delete_note/1"

    def test_edit_link_is_available(self):
        self.driver.get(self.get_server_url() + "/upload/show_image/test.png")

        module_code = self.driver.find_element_by_class_name('module_code_data')
        module_code.send_keys("CS31310")

        lecturer_name = self.driver.find_element_by_class_name("lecturer_name")
        lecturer_name.send_keys("Mr Foo")

        location_name = self.driver.find_element_by_class_name('location_name')
        location_name.send_keys("C11 Hugh Owen")

        date = self.driver.find_element_by_class_name("date")
        date.send_keys("12th February 2016 16:00")

        title = self.driver.find_element_by_class_name("title")
        title.send_keys("Title")

        submit_button = self.driver.find_element_by_class_name('submit')
        submit_button.click()

        edit_form = self.driver.find_element_by_class_name("edit_note_form").get_attribute("action").split("http://localhost:5000")

        edit_link = self.driver.find_element_by_class_name('edit_note')

        assert edit_link.is_displayed() is True

        assert edit_form[1] == "/metadata/edit/1"
