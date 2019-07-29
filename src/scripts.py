from db import DB


products = [

	{
		"name": "PayPal",
		"category": "payment-gateway"
	},
	{
		"name": "Stripe Connect",
		"category": "payment-gateway"
	},
	{
		"name": "Apple Pay",
		"category": "payment-gateway"
	},
	{
		"name": "MyVirtualMerchant",
		"category": "payment-gateway"
	},
	{
		"name": "WePay",
		"category": "payment-gateway"
	},
	{
		"name": "Dwolla",
		"category": "payment-gateway"
	}
]

def remove_feedbacks(filter):
	DB().remove(DB.USER_FB, filter)

def insert_product(product):
	DB().insert(DB.PROD_CLXN, product)

# remove_feedbacks({})

# for product in products:
# 	insert_product(product)
