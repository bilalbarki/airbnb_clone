from app import app
from datetime import datetime
import unittest, json, logging, itertools
from app.models.base import db
from app.models.state import State

class StateTestCase(unittest.TestCase):
	
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)
		db.create_tables([State], safe = True)

	def tearDown(self):
		db.drop_table(State)

	def state_dict(self, name = None):
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

	def test_create(self):
		cases = ["Ohio", "Ohio", None]
		count = 1
		for case in cases:
			state_dictionary = self.state_dict(case)
			jsonified, status = self.create_state_and_return_json(state_dictionary)
			
			if count == 2:
				self.assertEqual(jsonified['code'], 10001)
			elif case == cases[0]:
				self.assertEqual(jsonified['name'], case)
				self.assertEqual(jsonified['id'], count)
			else:
				self.assertFalse("id" in jsonified.keys())
			count+=1

	def test_list(self):
		resp = self.app.get('/states')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 0)
		state_dictionary = self.state_dict("Ohio")
		jsonified, status = self.create_state_and_return_json(state_dictionary)
		resp = self.app.get('/states')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 1)

	def test_get(self):
		name = "Ohio"
		state_dictionary = self.state_dict(name)
		time_now = datetime.now().strftime("%Y/%m/%d %H:%M")
		jsonified, status = self.create_state_and_return_json(state_dictionary)
		resp = self.app.get('/states/1')
		jsonified = json.loads(resp.data)
		self.assertEqual(resp.status_code, 200)
		set_keys_state = ["name"]
		set_keys_base = ["created_at", "updated_at", "id"]
		self.assertEqual(set(jsonified), set(set_keys_state + set_keys_base))
		self.assertEqual(jsonified['name'], name)
		#self.assertEqual(jsonified['created_at'][:-3], time_now)
		#self.assertEqual(jsonified['updated_at'][:-3], time_now)

		# check for non-existing state
		resp = self.app.get('/states/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())

	def test_delete(self):
		name = "Ohio"
		state_dictionary = self.state_dict(name)
		jsonified, status = self.create_state_and_return_json(state_dictionary)
		resp_before_del = self.app.get('/states')
		jsonified_before_del = json.loads(resp_before_del.data)
		resp = self.app.delete('/states/1')
		self.assertEqual(resp.status_code, 200)
		resp_after_del = self.app.get('/states')
		jsonified_after_del = json.loads(resp_after_del.data)
		self.assertEqual(len(jsonified_before_del['data']), 1)
		self.assertEqual(len(jsonified_after_del['data']), 0)

		# testing non-existent delete
		resp = self.app.delete('/states/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())