from ssl import Options
from flask.wrappers import Response
from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from fwtapp import app, db, index

class TestBase(LiveServerTestCase):
    def create_app(self):

        app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///test.db"
        app.config["LIVESERVER_PORT"]=5050
        app.config["SECRET_KEY"] = "fgsahfdfbnvny"
        app.config["DEBUG"]=True
        app.config["TESTING"]=True
        return app

    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(Options=chrome_options)

        db.create_all()

        self.driver.get("http://localhost:5000")

    def tearDown(self):
        self.driver.quit()
        db.drop_all()

    def test_server_running(self):
        response = urlopen("http://localhost:5000")
        self.assertEqual(response.code, 200)

class TestViews(TestBase):

    def test_home_get(self):
        self.driver.find_element_by_xpath("/html/body/h4/a[1]").click()
        self.assertIn(url_for("index"), self.driver.current_url)

    def test_add_character_get(self):
        self.driver.find_element_by_xpath("/html/body/h4/a[2]").click()
        self.assertIn(url_for("newcharacter"), self.driver.current_url)

    def test_add_location_get(self):
        self.driver.find_element_by_xpath("/html/body/h4/a[3]").click()
        self.assertIn(url_for("newlocation"), self.driver.current_url)

    def test_journey_get(self):
        self.driver.find_element_by_xpath("/html/body/h4/a[4]").click()
        self.assertIn(url_for("journey"), self.driver.current_url)
    
    def test_encounters_get(self):
        self.driver.find_element_by_xpath("/html/body/h4/a[5]").click()
        self.assertIn(url_for("encounters"), self.driver.current_url)