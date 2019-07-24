from db		import DB

class Product:

	def __init__(self):
		self.val = {
			'Y':1,
			'N':-1
		}

	def update(self, user, fb, product):
		data = {
			'email_id'	: user.get('email_id'),
			'persona'	: user.get('persona'),
			'product_id': str(product.get('_id')),
			'value'		: self.val[fb]
		}
		DB().insert(DB.USER_FB, data)

	def list(self):
		return list(DB().find(DB.PROD_CLXN))