from db import DB


class Persona:

	def __init__(self):
		pass

	def list(self):
		return list(DB().find(DB.PERSONA_CLXN))
