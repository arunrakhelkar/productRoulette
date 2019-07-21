import json
import pandas as pd 
import numpy as np
import warnings

warnings.filterwarnings('ignore')

class Model:


	def __init__(self):
		conf = {}
		with open("config.json", 'r') as f:
			config = json.load(f)
		products = [product['name'] for product in config['product']]
		users = [user['name'] for user in config['user']]
		matrix = np.random.random_integers(-1,1,(len(products), len(users)))
		df = pd.DataFrame(data = matrix, index = products, columns = users)
		#print(df.to_string())
		self.matrix = df

	def get_matrix(self):
		conf = {}
		with open("config.json", 'r') as f:
			config = json.load(f)
		products = [product['name'] for product in config['product']]
		users = [user['name'] for user in config['user']]
		matrix = np.random.random_integers(-1,1,(len(products), len(users)))
		df = pd.DataFrame(data = matrix, index = products, columns = users)
		print(df.to_string())
		return df

	def get_similar_product(self, product):
		print(self.matrix[product])
		return self.matrix.corrwith(self.matrix[product])


a = Model()
print(a.get_similar_product('Salesforce'))
		