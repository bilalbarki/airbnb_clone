from app import app
from datetime import datetime
import unittest, json, logging, itertools
from app.models.base import db
from app.models.state import State
from app.models.city import City
from app.models.user import User
from app.models.place import Place

class PlaceTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)
		db.create_tables([User, State, City, Place], safe = True)

	def tearDown(self):
		db.drop_table(Place)
		db.drop_table(City)
		db.drop_table(State)
		db.drop_table(User)

	def name_dict(self, name = None):
		values = {}
		if name != None:
			values['name'] = name
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

	def test_create(self):
		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		
		true_cases = [
   			["testPlace", "", 4, 3, 8, 100, 2.0, 3.0, 1, 1],
   			["anotherPlace", "another description", None, None, None, None, 2.0, 3.0, 1, 1],
   		]
   		keys=["name", "description", "number_rooms", "number_bathrooms", "max_guest", "price_by_night", "latitude", "longitude", "owner_id", "city_id"]
   		
   		count = 1
   		for case in true_cases:
   			place_dictionary = self.place_dict(*case)
   			jsonified, status = self.create_place_and_return_json(place_dictionary)
   
   			#if case == true_cases[0]:
   			for key, value in zip(keys, case):
   				if value == None:
   					key_value = 0
   				else:
   					key_value = value
   				self.assertEqual(jsonified[key], key_value)
   			self.assertEqual(jsonified['id'], count)
   			count+=1


   	def test_list(self):
   		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()

		resp = self.app.get('/places')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 0)

   		true_case =["testPlace", "this is a description", 4, 3, 8, 100, 2.0, 3.0, 1, 1]
   			
   		place_dictionary = self.place_dict(*true_case)
   		jsonified, status = self.create_place_and_return_json(place_dictionary)
   		
   		resp = self.app.get('/places')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 1)

	def test_get(self):
		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()

		true_case =["testPlace", "this is a description", 4, 3, 8, 100, 2.0, 3.0, 1, 1]
   			
   		place_dictionary = self.place_dict(*true_case)
   		jsonified, status = self.create_place_and_return_json(place_dictionary)

   		resp = self.app.get('/places/1')
		jsonified = json.loads(resp.data)

		self.assertEqual(resp.status_code, 200)

		set_keys_place = ["name", "description", "number_rooms", "number_bathrooms", "max_guest", "price_by_night", "latitude", "longitude", "owner_id", "city_id"]
		set_keys_base = ["created_at", "updated_at", "id"]

		self.assertEqual(set(jsonified), set(set_keys_place + set_keys_base))
		
		self.assertEqual(jsonified['id'], 1)
		for key, value in zip(set_keys_place, true_case):
   			if value == None:
   				key_value = 0
   			else:
   				key_value = value
   			self.assertEqual(jsonified[key], key_value)

   	def test_delete(self):
   		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()

		true_case =["testPlace", "this is a description", 4, 3, 8, 100, 2.0, 3.0, 1, 1]
   			
   		place_dictionary = self.place_dict(*true_case)
   		jsonified, status = self.create_place_and_return_json(place_dictionary)

   		resp_before_del = self.app.get('/places')
		jsonified_before_del = json.loads(resp_before_del.data)

		resp = self.app.delete('/places/1')

		resp_after_del = self.app.get('/places')
		jsonified_after_del = json.loads(resp_after_del.data)
		self.assertEqual(len(jsonified_before_del), 1)
		self.assertEqual(len(jsonified_after_del), 0)

		# testing non-existent delete
		resp = self.app.delete('/places/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())

	def test_update(self):
		def update_place(id, update_dict):
			resp = self.app.put('/places/%d' % id, data=update_dict)
			jsonified = json.loads(resp.data)
			return jsonified, resp.status_code

		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()

		true_case =["testPlace", "this is a description", 4, 3, 8, 100, 2.0, 3.0, 1, 1]
   			
   		place_dictionary = self.place_dict(*true_case)
   		jsonified, status = self.create_place_and_return_json(place_dictionary)

   		update_values = [
			["testPlace2"], 
			[None, ""],
			[None, None, 5], 
			[None, None, None, 1], 
			[None, None, None, None, 7], 
			[None, None, None, None, None, 99], 
			[None, None, None, None, None, None, 5.0], 
			[None, None, None, None, None, None, None, 10.0],
			[None, None, None, None, None, None, None, None, 2],
			[None, None, None, None, None, None, None, None, None, 2],   
		]

		set_keys_place = ["name", "description", "number_rooms", "number_bathrooms", "max_guest", "price_by_night", "latitude", "longitude", "owner_id", "city_id"]
		set_keys_base = ["created_at", "updated_at", "id"]

		for update_list,key in zip(update_values, set_keys_place):
			update_dict = self.place_dict(*update_list)
			jsonified, status = update_place(1, update_dict)
			if key == "owner_id":
				self.assertEqual(jsonified[key], place_dictionary[key])
			elif key == "city_id":
				self.assertEqual(jsonified[key], place_dictionary[key])
			else:
				self.assertEqual(jsonified[key], update_dict[key])

		packaged_update_values = ["Placetest", "another description", 10, 6, 15, 102, 15.0, 26.0, 4, 4]
		update_dict = self.place_dict(*packaged_update_values)
		jsonified, status = update_place(1, update_dict)
		for key in set_keys_place:
			if key == "owner_id":
				self.assertEqual(jsonified[key], place_dictionary[key])
			elif key == "city_id":
				self.assertEqual(jsonified[key], place_dictionary[key])
			else:
				self.assertEqual(jsonified[key], update_dict[key])

		# testing non-existent put request
		jsonified, status = update_place(100, update_dict)
		self.assertFalse("id" in jsonified.keys())

	# route /states/<state_id>/cities/<city_id>/places
	def create_place_by_place_city(self, state_id, city_id, update_dict):
		resp = self.app.post('/states/%d/cities/%d/places' % (state_id, city_id), data=update_dict)
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code

	def test_create_second(self):
		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()

		true_cases = [
   			["testPlace", "", 4, 3, 8, 100, 2.0, 3.0, 1],
   			#["anotherPlace", "another description", None, None, None, None, 2.0, 3.0, 1],
   		]
   		keys=["name", "description", "number_rooms", "number_bathrooms", "max_guest", "price_by_night", "latitude", "longitude", "owner_id"]
   		
   		count = 1
   		for case in true_cases:
   			place_dictionary = self.place_dict(*case)
   			jsonified, status = self.create_place_by_place_city(1, 1, place_dictionary)
   
   			for key, value in zip(keys, case):
   				if value == None:
   					key_value = 0
   				else:
   					key_value = value
   				self.assertEqual(jsonified[key], key_value)
   			self.assertEqual(jsonified['id'], count)
   			count+=1

   	# route /states/<state_id>/cities/<city_id>/places
	def test_list_second(self):
		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()

		resp = self.app.get('/states/1/cities/1/places')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 0)

   		true_case = ["testPlace", "", 4, 3, 8, 100, 2.0, 3.0, 1]
   			
   		place_dictionary = self.place_dict(*true_case)
   		jsonified, status = self.create_place_by_place_city(1, 1, place_dictionary)
   		
   		resp = self.app.get('/states/1/cities/1/places')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified), 1)


