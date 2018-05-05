from pymongo import MongoClient
from bson.objectid import ObjectId
import json


class UserModel:
    def __init__(self):
        config = json.load(open("./config.json", "r"))
        client = MongoClient(config["host"], config["port"])
        self.db = client[config["mongo_db"]]

    def add_new_user(self, name, email, username, password):
        user = {
            'name': name,
            'email': email,
            'username': username,
            'password': password,
            'cart': []
        }
        self.db.users.insert_one(user)

    def authenticate(self, username, password):
        query = {
            'username': username,
            'password': password
        }
        cursor = self.db.users.find(query)
        if cursor.count() == 0:
            return False
        else:
            return True

    def get_by_username(self, username):
        query = {
            'username': username
        }
        cursor = self.db.users.find(query)
        if cursor.count() == 0:
            return None
        for user in cursor:
            return user

    def add_product_to_cart(self, user_id, product_id):
        condition = {'_id': ObjectId(user_id)}

        cursor = self.db.users.find(condition)

        user_data = cursor[0] if cursor.count() > 0 else None
        if user_data is None:
            return False

        # to support old users
        if 'cart' not in user_data:
            user_data['cart'] = []

        # add product only if it hasnt been added in the past
        if product_id not in user_data['cart']:
            user_data['cart'].append(product_id)
            self.db.users.update_one(filter=condition, update={'$set': user_data})

        return True

    def get_by_id(self, _id):
        query = {
            '_id': ObjectId(_id)
        }
        cursor = self.db.users.find(query)
        user = cursor[0] if cursor.count() > 0 else None
        return user

    def get_cart(self, _id):
        query = {
            '_id': ObjectId(_id)
        }
        cursor = self.db.users.find(query)
        cart = cursor[0]['cart'] if cursor.count() > 0 else None
        return cart

    def remove_product_from_cart(self, user_id, product_id):
        cart = self.get_cart(user_id)
        cart.remove(product_id)

        condition = dict()
        condition['_id'] = ObjectId(user_id)

        self.db.users.update_one(filter=condition, update={'$set': {'cart': cart}})

        return cart
