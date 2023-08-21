from pymongo import MongoClient
import json
from flask import jsonify
from bson import ObjectId

class user_model():
    def __init__(self):
        self.client=MongoClient('mongodb://localhost:27017')
        self.db=self.client['UserData']
        print('Connection Sucessful')
        
    def superuser(self,username,password):
        
        self.collection=self.db['superuser']
        data=self.collection.find({'username':username})
        return data
    
    def details(self,username,role):
        self.collection=self.db[role]
        data=self.collection.find({'username':username})
        return data

        