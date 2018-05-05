from pymongo import MongoClient
import re
from bson.objectid import ObjectId
import json

class ProductModel:
    def __init__(self):
        config = json.load(open("./config.json", "r"))
        client = MongoClient(config["mongo_host"], config["mongo_port"])
        self.db = client[config["mongo_db"]]

    def save(self, product):
        self.db.products.insert_one(product)

    def search_by_name(self, name):
        query = {
            'name': re.compile(name, re.IGNORECASE)
        }
        result = self.db.products.find(query)
        matches = []
        for product in result:
            matches.append(product)
        return matches

    def delete_by_id(self, _id):
        self.db.products.delete_one({'_id': ObjectId(_id)})

    def update_by_id(self, _id, updated_product):
        condition = dict()
        condition['_id'] = ObjectId(_id)

        self.db.products.update_one(filter=condition, update={'$set': updated_product})

    def get_product(self, _id):
        query = {
            '_id': ObjectId(_id)
        }
        cursor = self.db.products.find(query)
        product = cursor[0] if cursor.count() > 0 else None
        return product
