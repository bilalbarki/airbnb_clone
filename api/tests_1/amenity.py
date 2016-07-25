from app import app
from datetime import datetime
import unittest, json, logging, itertools
from app.models.base import db
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from app.models.place import Place
from app.models.state import State
from app.models.city import City
from app.models.user import User

class AmenitiesTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)
		db.create_tables([User, State, City, Place, Amenity, PlaceAmenities], safe = True)

	def tearDown(self):
		db.drop_table(PlaceAmenities)
		db.drop_table(Place)
		db.drop_table(City)
		db.drop_table(State)
		db.drop_table(User)
		db.drop_table(Amenity)
		

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
		return resp

	def create_amenity(self, state_dict):
		return self.app.post('/amenities', data=state_dict)

	def create_amenity_and_return_json(self, amenity_dictionary):
		resp = self.create_amenity(amenity_dictionary)
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code

	def create_place_rows(self):
		true_case =["testPlace", "this is a description", 4, 3, 8, 100, 2.0, 3.0, 1, 1]		
   		place_dictionary = self.place_dict(*true_case)
   		jsonified, status = self.create_place_and_return_json(place_dictionary)
   		return jsonified, status

	def test_create(self):
		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		self.create_place_rows()
		cases = ["Feature", "Feature", None]
		count = 1
		for case in cases:
			amenity_dictionary = self.name_dict(case)
			jsonified, status = self.create_amenity_and_return_json(amenity_dictionary)
			
			if count == 2:
				self.assertEqual(jsonified['code'], 10003)
			elif case == cases[0]:
				self.assertEqual(jsonified['name'], case)
				self.assertEqual(jsonified['id'], count)
			else:
				self.assertFalse("id" in jsonified.keys())
			count+=1

		# cases = [None, 1, 1]

		# PlaceAmenities_dict = {
		# 	"place_id": 1,
		# 	"amenity_id": 1,
		# }

		# amenity_dictionary = self.name_dict(*cases)
		
		# jsonified, status = self.create_amenity_and_return_json(amenity_dictionary)

		# resp = self.app.get('/places/1/amenities')
		# print resp.data

	def test_list(self):
		def get_amenities():
			return self.app.get('/amenities')

		resp = get_amenities()
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 0)
		amenity_dictionary = self.name_dict("testing")
		jsonified, status = self.create_amenity_and_return_json(amenity_dictionary)
		resp = get_amenities()
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 1)		

	def test_delete(self):
		def get_amenities():
			return self.app.get('/amenities')

		amenity_dictionary = self.name_dict("testing")
		jsonified, status = self.create_amenity_and_return_json(amenity_dictionary)
		resp_before_del = get_amenities()
		jsonified_before_del = json.loads(resp_before_del.data)
		resp = self.app.delete('/amenities/1')
		self.assertEqual(resp.status_code, 200)
		resp_after_del = get_amenities()
		jsonified_after_del = json.loads(resp_after_del.data)
		self.assertEqual(len(jsonified_before_del), 1)
		self.assertEqual(len(jsonified_after_del), 0)

		# testing non-existent delete
		resp = self.app.delete('/amenities/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())

	def test_get_second(self):
		def get_amenities(place_id):
			return self.app.get('/places/%d/amenities' % place_id)

		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		self.create_place_rows()
		amenity_dictionary = self.name_dict("testing")
		jsonified, status = self.create_amenity_and_return_json(amenity_dictionary)

		resp = get_amenities(1)
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 0)
		
		cases = [None, 1, 1]
		amenity_dictionary = self.name_dict(*cases)
		jsonified, status = self.create_amenity_and_return_json(amenity_dictionary)

		resp = get_amenities(1)
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 1)	




