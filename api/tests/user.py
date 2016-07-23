from app import app
from app.models.base import db
from app.models.user import User
from datetime import datetime
import json
import unittest
import logging
import peewee

class UserTestCase(unittest.TestCase):

    # create a test client of app
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        logging.disable(logging.CRITICAL)

        db.connect()
        db.create_tables([User])

    def tearDown(self):
        db.drop_table(User) 

    # create function to send post request to /users
    def create(self, first_name, last_name, email, password):
        return self.app.post('/users', data=dict(first_name=first_name, last_name=last_name, email=email, password=password))

    # test cases for data that might get sent for creating a User
    def test_create(self):
        response = self.create('Jon', 'Snow', 'jon@snow.com', 'toto1234')
        print response.data
        assert '"id": 1,' in response.data
        #response = self.create('Jon', 'Snow', 'jon@snow.com')
        #response = self.create('Jon', 'Snow', 'toto1234')
        #response = self.create('Jon', 'jon@snow.com', 'toto1234')
        #response = self.create('Snow', 'jon@snow.com', 'toto1234')
