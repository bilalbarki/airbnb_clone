from app import app
from datetime import datetime
import json
import unittest

class TestCase(unittest.TestCase):

    # create a test client of app
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        def tearDown(self):
            pass 

    # check HTTP response code for sending GET request to '/'
    def test_200(self):
        response = self.app.get('/')
        self.assertEquals(response.status_code, 200)

    # check if the status is OK in the json response
    def test_status(self):
        response = self.app.get('/')
        assert '"status": "OK"' in response.data

    # check if the 'time' key in json response matches now-time
    def test_time(self):
        response = self.app.get('/')
        assert '"time": "%s' % datetime.now().strftime("%Y/%m/%d %H:%M") in response.data

    # check if the 'utc_time' key in json response matches now-time
    def test_time_utc(self):
        response = self.app.get('/')
        assert '"utc_time": "%s' % datetime.utcnow().strftime("%Y/%m/%d %H:%M") in response.data
