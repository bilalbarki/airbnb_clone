from app import app
from datetime import datetime
import unittest, json, logging, itertools
from app.models.base import db
from app.models.state import State
from app.models.city import City

class CityTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)
		db.create_tables([State, City], safe = True)

	def tearDown(self):
		db.drop_table(City)
		db.drop_table(State)

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

	def test_create(self):
		self.create_state_rows()
		cases = ["Toledo", "Toledo", None]
		count = 1
		for case in cases:
			city_dictionary = self.name_dict(case)
			jsonified, status = self.create_city_and_return_json(1, city_dictionary)
			
			if count == 2:
				self.assertEqual(jsonified['code'], 10002)
			elif case == cases[0]:
				self.assertEqual(jsonified['name'], case)
				self.assertEqual(jsonified['id'], count)
			else:
				self.assertFalse("id" in jsonified.keys())
			count+=1

	def test_list(self):
		self.create_state_rows()

		resp = self.app.get('/states/1/cities')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 0)
		city_dictionary = self.name_dict("Toledo")
		jsonified, status = self.create_city_and_return_json(1, city_dictionary)
		resp = self.app.get('/states/1/cities')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 1)

		resp = self.app.get('/states/2/cities')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 0)
		city_dictionary = self.name_dict("TestCity")
		jsonified, status = self.create_city_and_return_json(2, city_dictionary)
		resp = self.app.get('/states/2/cities')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 1)

	def test_get(self):
		self.create_state_rows()
		name = "Toledo"
		city_dictionary = self.name_dict(name)
		jsonified, status = self.create_city_and_return_json(1, city_dictionary)
		resp = self.app.get('/states/1/cities/1')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 200)
		set_keys_state = ["name", "state_id"]
		set_keys_base = ["created_at", "updated_at", "id"]
		self.assertEqual(set(jsonified), set(set_keys_state + set_keys_base))
		self.assertEqual(jsonified['name'], name)

		# check for non-existing city
		resp = self.app.get('/states/1/cities/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())

	def test_delete(self):
		self.create_state_rows()

		name = "Toledo"
		city_dictionary = self.name_dict(name)
		jsonified, status = self.create_city_and_return_json(1, city_dictionary)
		resp_before_del = self.app.get('/states/1/cities')
		jsonified_before_del = json.loads(resp_before_del.data)
		resp = self.app.delete('/states/1/cities/1')
		self.assertEqual(resp.status_code, 200)
		resp_after_del = self.app.get('/states/1/cities')
		jsonified_after_del = json.loads(resp_after_del.data)
		self.assertEqual(len(jsonified_before_del['data']), 1)
		self.assertEqual(len(jsonified_after_del['data']), 0)

		# testing non-existent delete
		resp = self.app.delete('/states/1/cities/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())