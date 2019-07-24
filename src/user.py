
from persona import Persona
#from product import Product
from db import DB

class User():

	def __init__(self):
		pass
	
	def get(self, email_id):
		users = list(DB().find(DB.USERS_CLXN))
		user = next((x for x in users if x['email_id'] == email_id), None)
		return user

	def add(self, persona, email_id):
		data = {
			'email_id': email_id,
			'persona' : persona
		}
		DB().insert(DB.USERS_CLXN, data)

	def list(self, filter):
		return list(DB().find(DB.USERS_CLXN,filter))
