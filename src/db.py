import json
import pymongo

from env import ENV


class DB():

    USERS_CLXN  = "users"
    PERSONA_CLXN = "persona"
    PROD_CLXN   = "products"
    USER_FB     = "user_feedback"

    mongoc = pymongo.MongoClient(ENV['MONGO_URI'])

    def __init__(self):
        self.db = self.mongoc[ENV['DB']]

    def find(self, clxn, filter = {}, projection = {}, docs_cnt = 0):
        return self.db[clxn].find(filter).limit(docs_cnt)

    def find_one(self, clxn, filter = {}):
        return self.db[clxn].find_one(filter)

    def update_one(self, clxn, filter, update):
        return self.db[clxn].update_one(filter, update)

    def insert(self, clxn, data):
        return self.db[clxn].insert(data)