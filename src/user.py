
from persona import Persona
#from product import Product
from db import DB

class User():

	def __init__(self, email_id):
		self.email_id = email_id
	
	def get(self):
		users = list(DB().find(DB.USERS_CLXN))
		user = next((x for x in users if x['email_id'] == self.email_id), None)
		return user

	def add(self, persona):
		data = {
			'email_id':self.email_id,
			'persona' :persona
		}
		DB().insert(DB.USERS_CLXN, data)
