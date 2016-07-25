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
        return self.app.post('/users', data=dict(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            password=password))

    # test cases for data that might get sent for creating a User
    def test_create(self):

        response = self.create('Jon', 'Snow', 'jon@snow.com', 'toto1234')
        parsed_json = json.loads(response.data)
        self.assertEqual(parsed_json['id'], 1) # assert parsed_json['id'] == 1

        # test cases of missing parameters, should return 400 error code
        ''' note: we would also check json msg and error code, but project 
            does not specify what these should be '''
        response = self.app.post('/users', data=dict(
            first_name='Kate', 
            last_name='Snow', 
            email='kate1@snow.com'
        ))
        self.assertEqual(response.status_code, 400)        

        response = self.app.post('/users', data=dict(
            first_name='Kate', 
            last_name='Snow', 
            password='abcd1234'
        ))
        self.assertEqual(response.status_code, 400)        

        response = self.app.post('/users', data=dict(
            first_name='Kate', 
            email='kate3@snow.com', 
            password='abcd1234'
        ))
        self.assertEqual(response.status_code, 400)        

        response = self.app.post('/users', data=dict(
            last_name='Snow', 
            email='kate4@snow.com', 
            password='abcd1234'
        ))
        self.assertEqual(response.status_code, 400)        

        # test proper response is generated for duplicate email
        response = self.create('Kate', 'Snow', 'jon@snow.com', 'abcd1234')
        self.assertEquals(response.status_code, 409)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['code'], 10000)
        self.assertEqual(json_response['msg'], "Email already exists")      
