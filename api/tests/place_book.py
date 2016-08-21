from app import app
from datetime import datetime
import unittest, json, logging, itertools
from app.models.base import db
from app.models.state import State
from app.models.city import City
from app.models.user import User
from app.models.place import Place
from app.models.place_book import PlaceBook

class PlaceBookTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)
		db.create_tables([User, State, City, Place, PlaceBook], safe = True)

	def tearDown(self):
		db.drop_table(PlaceBook)
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

	def placebook_dict(self, user_id = None, is_validated = None, date_start = None, number_nights = None):
		values = {}
		if user_id != None:
			values['user_id'] = user_id
		if is_validated != None:
			values['is_validated'] = is_validated
		if date_start != None:
			values['date_start'] = date_start
		if number_nights != None:
			values['number_nights'] = number_nights
		return values

	def create_placebook(self, place_id, placebook_dict):
		resp = self.app.post('/places/%d/books' % place_id, data=placebook_dict)
		return resp

	def create_placebook_and_return_json(self, place_id, placebook_dict):
		resp = self.create_placebook(place_id, placebook_dict)
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
		
		true_cases = [
   			[1, True, "2016/08/18 01:33:29", 3],
   			[1, None, "2017/08/18 01:33:29", None],
   		]
   		keys = ["user_id", "is_validated", "date_start", "number_nights"]

   		count = 1
   		for case in true_cases:
   			placebook_dictionary = self.placebook_dict(*case)
   			jsonified, status = self.create_placebook_and_return_json(1, placebook_dictionary)
   
   			for key, value in zip(keys, case):
   				if key == "is_validated" and value == None:
   					key_value = False
   				elif value == None:
   					key_value = 1
   				else:
   					key_value = value
   				self.assertEqual(jsonified[key], key_value)
   			self.assertEqual(jsonified['id'], count)
   			count+=1

   		# check booking overlap
   		placebook_dictionary = self.placebook_dict(*true_cases[0])
   		jsonified, status = self.create_placebook_and_return_json(1, placebook_dictionary)
   		self.assertEqual(jsonified['code'], 110000)
   		self.assertEqual(status, 410)

   	def test_list(self):
   		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		self.create_place_rows()
		time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		true_case = [1, True, time, 3]

		resp = self.app.get('/places/1/books')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 0)

		placebook_dictionary = self.placebook_dict(*true_case)
   		jsonified, status = self.create_placebook_and_return_json(1, placebook_dictionary)

   		resp = self.app.get('/places/1/books')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 1)

	# route /places/<place_id>/books/<book_id>
	def test_get(self):
		def get_placebook_and_return_json(place_id, book_id):
			resp = self.app.get('/places/%d/books/%d' % (place_id, book_id))
			jsonified = json.loads(resp.data)
			return jsonified, resp.status_code 


		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		self.create_place_rows()

		time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		true_case = [1, True, time, 3]

		placebook_dictionary = self.placebook_dict(*true_case)
   		jsonified, status = self.create_placebook_and_return_json(1, placebook_dictionary)

   		jsonified, status = get_placebook_and_return_json(1,1, )
   		self.assertEqual(status, 200)

   		set_keys_place = ["user_id", "is_validated", "date_start", "number_nights", "place_id"]
		set_keys_base = ["created_at", "updated_at", "id"]

		self.assertEqual(set(jsonified), set(set_keys_place + set_keys_base))
		self.assertEqual(jsonified['id'], 1)

		for key, value in map(None,set_keys_place, true_case):
   			if key == "place_id":
   				key_value = 1
   			elif value == None:
   				if key == "is_validated":
   					key_value = False
   				else:
   					key_value = 1
   			else:
   				key_value = value
   			self.assertEqual(jsonified[key], key_value)

   	def test_update(self):
   		def update_placebook(place_id, book_id, placebook_dict):
			resp = self.app.put('/places/%d/books/%d' % (place_id, book_id), data=placebook_dict)
			jsonified = json.loads(resp.data)
			return jsonified, resp.status_code

		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		self.create_place_rows()

		time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		true_case = [1, True, time, 3]

		placebook_dictionary = self.placebook_dict(*true_case)
   		jsonified, status = self.create_placebook_and_return_json(1, placebook_dictionary)

   		time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

   		update_values = [
			[2], 
			[None, False],
			[None, None, time], 
			[None, None, None, 4], 
		]

		set_keys_place = ["user_id", "is_validated", "date_start", "number_nights"]
		set_keys_base = ["created_at", "updated_at", "id"]

		for update_list,key in zip(update_values, set_keys_place):
			update_dict = self.placebook_dict(*update_list)
			jsonified, status = update_placebook(1, 1, update_dict)
			if key == "user_id":
				self.assertEqual(jsonified[key], placebook_dictionary[key])
			else:
				self.assertEqual(jsonified[key], update_dict[key])
			self.assertEqual(jsonified['place_id'], 1)

	def test_delete(self):
		self.create_state_rows()
		self.create_city_rows()
		self.create_user_rows()
		self.create_place_rows()

		time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		true_case = [1, True, time, 3]

		placebook_dictionary = self.placebook_dict(*true_case)
   		jsonified, status = self.create_placebook_and_return_json(1, placebook_dictionary)

   		resp_before_del = self.app.get('/places/1/books')
		jsonified_before_del = json.loads(resp_before_del.data)

		resp = self.app.delete('/places/1/books/1')
		self.assertEqual(resp.status_code, 200)
		
		resp_after_del = self.app.get('/places/1/books')
		jsonified_after_del = json.loads(resp_after_del.data)
		self.assertEqual(len(jsonified_before_del['data']), 1)
		self.assertEqual(len(jsonified_after_del['data']), 0)

		# testing non-existent delete
		resp = self.app.delete('/places/1/books/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())
