from app import app
from datetime import datetime
import unittest, json, logging, itertools
from app.models.base import db
from app.models.state import State
from app.models.city import City
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.review_place import ReviewPlace
from app.models.review_user import ReviewUser

class ReviewTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)
		db.create_tables([User, State, City, Place, Review, ReviewPlace, ReviewUser], safe = True)

	def tearDown(self):
		db.drop_table(ReviewPlace)
		db.drop_table(ReviewUser)
		db.drop_table(Review)
		db.drop_table(Place)
		db.drop_table(City)
		db.drop_table(State)
		db.drop_table(User)
		

	def name_dict(self, name = None, place_id = None, amenity_id = None):
		values = {}
		if name != None:
			values['name'] = name
		if place_id != None:
			values['place_id'] = place_id
		if amenity_id != None:
			values['amenity_id'] = amenity_id
		return values

	def create_state(self, state_dict):
		return self.app.post('/states', data=state_dict)

	def create_state_and_return_json(self, state_dictionary):
		resp = self.create_state(state_dictionary)
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code

	def create_city(self, id, state_dict):
		return self.app.post('/states/%d/cities' % id, data=state_dict)

	def create_city_and_return_json(self, id, state_dictionary):
		resp = self.create_city(id, state_dictionary)
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code

	def create_state_rows(self):
		state_dictionary = self.name_dict("Ohio")
		jsonified, status = self.create_state_and_return_json(state_dictionary)
		state_dictionary = self.name_dict("Florida")
		jsonified, status = self.create_state_and_return_json(state_dictionary)

	def create_city_rows(self):
		city_dictionary = self.name_dict("Toledo")
		jsonified, status = self.create_city_and_return_json(1, city_dictionary)
		city_dictionary = self.name_dict("TestCity")
		jsonified, status = self.create_city_and_return_json(2, city_dictionary)

	def place_dict(self, name = None, description = None, number_rooms = None, number_bathrooms = None, max_guest = None, price_by_night = None, latitude = None, longitude = None, owner_id = None, city_id = None):
		values = {}
		if name != None:
			values['name'] = name
		if description != None:
			values['description'] = description
		if number_rooms != None:
			values['number_rooms'] = number_rooms
		if number_bathrooms != None:
			values['number_bathrooms'] = number_bathrooms
		if max_guest != None:
			values['max_guest'] = max_guest
		if price_by_night != None:
			values['price_by_night'] = price_by_night
		if latitude != None:
			values['latitude'] = latitude
		if longitude != None:
			values['longitude'] = longitude
		if owner_id != None:
			values['owner_id'] = owner_id
		if city_id != None:
			values['city_id'] = city_id
		return values

	def create_place(self, state_dictionary):
		return self.app.post('/places', data=state_dictionary)

	def create_place_and_return_json(self, state_dictionary):
		resp = self.create_place(state_dictionary)
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code

	def create_user_rows(self):
		user_dict = {"first_name": "Jon", "last_name": "Snow", "email":"jon@snow.com", "password": "toto1234"}
		resp = self.app.post('/users', data=user_dict)

		user_dict = {"first_name": "Test", "last_name": "Rain", "email":"rain@test.com", "password": "toto1234"}
		resp = self.app.post('/users', data=user_dict)
		return resp

	def create_place_rows(self):
		true_case =["testPlace", "this is a description", 4, 3, 8, 100, 2.0, 3.0, 1, 1]		
   		place_dictionary = self.place_dict(*true_case)
   		jsonified, status = self.create_place_and_return_json(place_dictionary)
   		return jsonified, status

	def review_dict(self, message = None, stars = None, from_user_id = None):
		values = {}
		if message != None:
			values['message'] = message
		if stars != None:
			values['stars'] = stars
		if from_user_id != None:
			values['from_user_id'] = from_user_id
		return values


	def create_review(self, user_id, review_dictionary):
		return self.app.post('/users/%d/reviews' % user_id, data=review_dictionary)

	def create_review_and_return_json(self, user_id, review_dictionary):
		resp = self.create_review(user_id, review_dictionary)
		#print resp.data
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code

	def test_get(self):
		self.create_user_rows()

		resp = self.app.get('/users/100/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 404)

		resp = self.app.get('/users/1/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 0)

		true_case =["test review", 1, 1]
		review_dictionary = self.review_dict(*true_case)
		jsonified, status = self.create_review_and_return_json(1, review_dictionary)

		resp = self.app.get('/users/1/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 1)

	def test_post(self):
		true_case =["test review", 1, 1]
		review_dictionary = self.review_dict(*true_case)
		jsonified, status = self.create_review_and_return_json(1, review_dictionary)
		self.assertEqual(status, 404)

		true_cases = [
   			["test review", 1, 1],
   			["test review", None, 1]
   		]

   		keys = ["message", "stars", "to_user_id"]

   		count = 1
   		for case in true_cases:
   			review_dictionary = self.review_dict(*true_case)
			jsonified, status = self.create_review_and_return_json(1, review_dictionary)
   
   			
   			for key in jsonified:
   				if key == 'message':
   					self.assertEqual(jsonified[key], true_cases[count-1][0])
   				if key == 'stars':
   					if true_cases[count-1][1] != None:
   						self.assertEqual(jsonified[key], true_cases[count-1][1])
   					else:
   						self.assertEqual(jsonified[key], 0)
   				if key == 'to_user_id':
   					self.assertEqual(jsonified[key], true_cases[count-1][2])
   				if key == 'id':
   					self.assertEqual(jsonified[key], count)
   			self.tearDown()
   			self.setUp()
   			count+=1

   	def test_get_by_review_id(self):
		self.create_user_rows()

		resp = self.app.get('/users/100/reviews/1')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 404)

		resp = self.app.get('/users/100/reviews/1')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 404)

		true_cases =["test review", 1, 1]
		review_dictionary = self.review_dict(*true_cases)
		jsonified, status = self.create_review_and_return_json(1, review_dictionary)
		
		for key in jsonified:
   			if key == 'message':
   				self.assertEqual(jsonified[key], true_cases[0])
   			if key == 'stars':
				self.assertEqual(jsonified[key], true_cases[1])
   			if key == 'to_user_id':
   				self.assertEqual(jsonified[key], true_cases[2])
   			if key == 'id':
   				self.assertEqual(jsonified[key], 1)

   		resp = self.app.get('/users/1/reviews/100')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 404)

	def test_delete_by_review_id(self):
		self.create_user_rows()

		resp = self.app.delete('/users/100/reviews/1')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 404)

		true_case =["test review", 1, 1]
		review_dictionary = self.review_dict(*true_case)
		jsonified, status = self.create_review_and_return_json(1, review_dictionary)

		resp = self.app.get('/users/1/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 1)

		resp = self.app.delete('/users/1/reviews/1')
		self.assertEqual(resp.status_code, 200)
		
		resp = self.app.get('/users/1/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 0)
		


	def create_review_by_places(self, place_id, review_dictionary):
		return self.app.post('/places/%d/reviews' % place_id, data=review_dictionary)

	def create_review_by_place_and_return_json(self, place_id, review_dictionary):
		resp = self.create_review_by_places(place_id, review_dictionary)
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code


	def test_get_by_place(self):
		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		self.create_place_rows()

		resp = self.app.get('/places/100/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 404)

		resp = self.app.get('/places/1/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 0)

		true_case =["test review", 1, 1]
		review_dictionary = self.review_dict(*true_case)
		jsonified, status = self.create_review_by_place_and_return_json(1, review_dictionary)

		resp = self.app.get('/places/1/reviews')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 1)

	# def test_post_by_place(self):
	# 	self.create_state_rows()
	# 	self.create_city_rows()
	# 	self.create_user_rows()
	# 	self.create_place_rows()


	# 	true_case =["test review", 1, 1]
	# 	review_dictionary = self.review_dict(*true_case)
	# 	jsonified, status = self.create_review_by_place_and_return_json(100, review_dictionary)
	# 	self.assertEqual(status, 404)

	# 	true_cases = [
 #   			["test review", 1, 1],
 #   			["test review", None, 1]
 #   		]

 #   		keys = ["message", "stars", "to_user_id"]

 #   		count = 1
 #   		for case in true_cases:
 #   			review_dictionary = self.review_dict(*true_case)
	# 		jsonified, status = self.create_review_by_place_and_return_json(1, review_dictionary)
   
   			
 #   			for key in jsonified:
 #   				if key == 'message':
 #   					self.assertEqual(jsonified[key], true_cases[count-1][0])
 #   				if key == 'stars':
 #   					if true_cases[count-1][1] != None:
 #   						self.assertEqual(jsonified[key], true_cases[count-1][1])
 #   					else:
 #   						self.assertEqual(jsonified[key], 0)
 #   				if key == 'to_place_id':
 #   					self.assertEqual(jsonified[key], true_cases[count-1][2])
 #   				if key == 'id':
 #   					self.assertEqual(jsonified[key], count)
 #   			self.tearDown()
 #   			self.setUp()
 #   			count+=1
