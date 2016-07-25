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

    # test list of Users is returned to a GET request with appropriate # elements:
    def test_list(self):
        # should return 0 elements if no user was created
        response = self.app.get('/users')
        parsed_json = json.loads(response.data)
        self.assertEqual(len(parsed_json), 0)
        
        # should return 1 element after a user is created
        self.create('Jon', 'Snow', 'jon@snow.com', 'toto1234')
        response = self.app.get('/users')
        parsed_json = json.loads(response.data)
        self.assertEqual(len(parsed_json), 1)

    # test retrieving a specific User at route /users/<user_id>:
    def test_get(self):
        created_at = datetime.now().strftime("%Y/%m/%d %H:%M")
        self.create('Jon', 'Snow', 'jon@snow.com', 'toto1234')
        response = self.app.get('/users/1')
        
        # check status code is 200:
        self.assertEqual(response.status_code, 200)
        
        # check data and time created is the same:
        parsed_json = json.loads(response.data)
        self.assertEqual(parsed_json['first_name'], 'Jon')
        self.assertEqual(parsed_json['last_name'], 'Snow')
        self.assertEqual(parsed_json['email'], 'jon@snow.com')
        self.assertEqual(parsed_json['created_at'][:-3], created_at)
        
        # check appropriate response when trying to get unknown user:
        response = self.app.get('/users/99')
        self.assertEqual(response.status_code, 404)
        parsed_json = json.loads(response.data)
        self.assertEqual(parsed_json['code'], 404)
        self.assertEqual(parsed_json['msg'], 'not found')

    # validate DELETE request on user ID at /users/<user_id>:
    def test_delete(self):
        self.create('Jon', 'Snow', 'jon@snow.com', 'toto1234')
        
        # number of User elements returned by GET req should be 1 now
        response = self.app.get('/users')
        parsed_json = json.loads(response.data)
        self.assertEqual(len(parsed_json), 1)
        
        # check the status code of deleting an element
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        
        # number of User elements returned by GET req should be 0 now
        response = self.app.get('/users')
        parsed_json = json.loads(response.data)
        self.assertEqual(len(parsed_json), 0)

        # check appropriate response when trying to get unknown user:
        response = self.app.delete('/users/99')
        self.assertEqual(response.status_code, 404)
        parsed_json = json.loads(response.data)
        self.assertEqual(parsed_json['code'], 404)
        self.assertEqual(parsed_json['msg'], 'not found')

    # validate PUT request to update record at /users/<user_id>:
    def test_update(self):
        self.create('Jon', 'Snow', 'jon@snow.com', 'toto1234')
        response = self.app.get('/users/1')
        parsed_json = json.loads(response.data)
        self.assertEqual(parsed_json['first_name'], 'Jon')
        self.assertEqual(parsed_json['last_name'], 'Snow')
        self.assertEqual(parsed_json['email'], 'jon@snow.com')

        response = self.app.put('/users/1', data=dict(
            first_name='Kate',
            last_name='Fire',
            email='kate@fire.com',
            password='abcd1234'
        ))
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get('/users/1')
        parsed_json = json.loads(response.data)
        self.assertEqual(parsed_json['first_name'], 'Kate')
        self.assertEqual(parsed_json['last_name'], 'Fire')
        self.assertEqual(parsed_json['email'], 'kate@fire.com')
