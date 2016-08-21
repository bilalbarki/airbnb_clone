from app import app
from datetime import datetime
import unittest, json, logging, itertools
from app.models.base import db
from app.models.user import User

class UserTestCase(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		logging.disable(logging.CRITICAL)
		db.create_tables([User], safe = True)

	def tearDown(self):
		db.drop_table(User)

	def user_dict(self, first_name = None, last_name = None, email = None, password = None, is_admin = None):
		values = {}
		if first_name != None:
			values['first_name'] = first_name
		if last_name != None:
			values['last_name'] = last_name
		if email != None:
			values['email'] = email
		if is_admin != None:
			values['is_admin'] = is_admin
		if password != None:
			values['password'] = password
		return values

	def create_user(self, user_dict):
		return self.app.post('/users', data=user_dict)

	def create_and_jsonify_user(self, data_set):
		user_dictionary = self.user_dict(*data_set)
		resp = self.create_user(user_dictionary)
		jsonified = json.loads(resp.data)
		return jsonified, resp.status_code

	def test_create(self):
   		true_cases = [
   			["Jon", "Snow", "jon@snow.com", "toto1234", True],
   			["Arya", "Stark", "arya@stark.com", "1122334a"]
   		]

   		false_cases = [
   			[['Jon',], ['Snow',], ['jon@snow.com',], ['toto1234',], [True,]],
			[['Jon', 'Snow'], ['Jon', 'jon@snow.com'], ['Jon', 'toto1234'], ['Jon', True], ['Snow', 'jon@snow.com'], ['Snow', 'toto1234'], ['Snow', True], ['jon@snow.com', 'toto1234'], ['jon@snow.com', True], ['toto1234', True]],
			[['Jon', 'Snow', 'jon@snow.com'], ['Jon', 'Snow', 'toto1234'], ['Jon', 'Snow', True], ['Jon', 'jon@snow.com', 'toto1234'], ['Jon', 'jon@snow.com', True], ['Jon', 'toto1234', True], ['Snow', 'jon@snow.com', 'toto1234'], ['Snow', 'jon@snow.com', True], ['Snow', 'toto1234', True], ['jon@snow.com', 'toto1234', True]],
			[['Jon', 'Snow', 'jon@snow.com', True], ['Jon', 'Snow', 'toto1234', True], ['Jon', 'jon@snow.com', 'toto1234', True], ['Snow', 'jon@snow.com', 'toto1234', True]],
		]

		duplicate_email_case = ["Jon", "Snow", "jon@snow.com", "toto1234", True]
		
		id_count = 1
		for data_set in true_cases:
			jsonified, status = self.create_and_jsonify_user(data_set)
			self.assertEqual(status, 200)
			self.assertEqual(jsonified['id'], id_count)
			if len(data_set) == 4:
				self.assertEqual(jsonified['is_admin'], False)
			id_count+=1

		user_dictionary = self.user_dict(*duplicate_email_case)
		resp = self.create_user(user_dictionary)
		jsonified = json.loads(resp.data)
		self.assertEqual(jsonified['code'], 10000)
		# might need to check error status
		'''for data_set in false_cases:
			key = False
			user_dictionary = self.user_dict(*data_set)
			resp = self.create_user(user_dictionary)
			jsonified = json.loads(resp.data)
			self.assertEqual(jsonified['id'], id_count)
			id_count+=1'''

	def test_list(self):
		resp = self.app.get('/users')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 0)
			
		true_case = ["Jon", "Snow", "jon@snow.com", "toto1234", True]
		user_dictionary = self.user_dict(*true_case)
		resp = self.create_user(user_dictionary)
		#jsonified = json.loads(resp.data)
		#self.assertEqual(len(jsonified), 7)
		
		resp = self.app.get('/users')
		jsonified = json.loads(resp.data)
		self.assertEqual(len(jsonified['data']), 1)

	def test_get(self):
		true_case = ["Jon", "Snow", "jon@snow.com", "toto1234", True]
		set_keys_user = ["first_name", "last_name", "email", "is_admin"]
		set_keys_base = ["created_at", "updated_at", "id"]
		user_dictionary = self.user_dict(*true_case)
		self.create_user(user_dictionary)
		resp = self.app.get('/users/1')
		self.assertEqual(resp.status_code, 200)
		jsonified = json.loads(resp.data)
		self.assertEqual(set(jsonified), set(set_keys_user + set_keys_base))
		true_case.remove("toto1234")
		for key, value in zip(set_keys_user, true_case):
			self.assertEqual(jsonified[key], value)

		# check for non-existing user
		resp = self.app.get('/users/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())

	def test_delete(self):
		true_case = ["Jon", "Snow", "jon@snow.com", "toto1234", True]
		user_dictionary = self.user_dict(*true_case)
		self.create_user(user_dictionary)
		resp_before_del = self.app.get('/users')
		jsonified_before_del = json.loads(resp_before_del.data)
		resp = self.app.delete('/users/1')
		self.assertEqual(resp.status_code, 200)
		resp_after_del = self.app.get('/users')
		jsonified_after_del = json.loads(resp_after_del.data)
		self.assertEqual(len(jsonified_before_del['data']), 1)
		self.assertEqual(len(jsonified_after_del['data']), 0)

		# testing non-existent delete
		resp = self.app.delete('/users/100')
		jsonified = json.loads(resp.data)
		self.assertFalse("id" in jsonified.keys())

	def test_update(self):
		#def update_user(id, update_dict):
		#	return self.app.put('/users/%d' % id, data=update_dict)

		def update_user(id, update_dict):
			resp = self.app.put('/users/%d' % id, data=update_dict)
			jsonified = json.loads(resp.data)
			return jsonified, resp.status_code
		
		true_case = ["Jon", "Snow", "jon@snow.com", "toto1234", True]
		user_dictionary = self.user_dict(*true_case)
		self.create_user(user_dictionary)
		update_values = [
			["Arya"], [None, "Stark"], [None, None, "arya@stark.com"], [None, None, None, "newpassword"], [None, None, None, None, False],
			#["Cercei", "Lynnister"],
			#["Sansa", "S.", "sansa@stark.com"],
			#["Neo", "Anderson", "neo@matrix.com", "onepassword"],
			#["James", "Cole", "james@cole.com", "12password", True],
		]
		set_keys_user = ["first_name", "last_name", "email", "password", "is_admin"]
		for update_list,key in zip(update_values, set_keys_user):
			update_dict = self.user_dict(*update_list)
			jsonified, status = update_user(1, update_dict)
			if key == "email":
				self.assertEqual(jsonified[key], user_dictionary[key])
			elif key == "password":
				self.assertEqual(status, 200)
			else:
				self.assertEqual(jsonified[key], update_dict[key])

		packaged_update_values = ["James", "Cole", "james@cole.com", "12password", True]
		update_dict = self.user_dict(*packaged_update_values)
		jsonified, status = update_user(1, update_dict)
		for key in set_keys_user:
			if key == "email":
				self.assertEqual(jsonified[key], user_dictionary[key])
			elif key == "password":
				self.assertEqual(status, 200)
			else:
				self.assertEqual(jsonified[key], update_dict[key])

		# testing non-existent put request
		jsonified, status = update_user(100, update_dict)
		self.assertFalse("id" in jsonified.keys())