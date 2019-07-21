
from .persona import Persona
from .product import Product


class User(Persona, Product):

	def __init__(self, id):

		self.id = id