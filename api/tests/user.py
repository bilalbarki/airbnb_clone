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
        #print response.data
        #assert '"id": 1,' in response.data
        new_user = User.get(User.id == 1)
        self.assertEqual(new_user.first_name, 'Jon');
        self.assertEqual(new_user.last_name, 'Snow');
        self.assertEqual(new_user.email, 'jon@snow.com');
        assert new_user.password is not None

        # test cases of missing parameters, should raise error:
        with self.assertRaises(TypeError):
            response = self.create('Jon', 'Snow', 'jon@snow.com')
        with self.assertRaises(TypeError):
            response = self.create('Jon', 'Snow', 'toto1234')
        with self.assertRaises(TypeError):
            response = self.create('Jon', 'jon@snow.com', 'toto1234')
        with self.assertRaises(TypeError):
            response = self.create('Snow', 'jon@snow.com', 'toto1234')

        response = self.create('Kate', 'Snow', 'jon@snow.com', 'abcd1234')
        #print response.data
        #with self.assertRaises(UserDoesNotExist):
        #    new_user = User.get(User.id == 2)
        self.assertEquals(response.status_code, 409)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['code'], 10000)
        self.assertEqual(json_response['msg'], "Email already exists")
        

        #response = self.create('Jon', 'Snow', 'jon@snow.com')
        #response = self.create('Jon', 'Snow', 'toto1234')
        #response = self.create('Jon', 'jon@snow.com', 'toto1234')
        #response = self.create('Snow', 'jon@snow.com', 'toto1234')
