from pymongo import MongoClient
import json
from flask import jsonify
from bson import ObjectId

class user_model():
    def __init__(self):
        self.client=MongoClient('mongodb://localhost:27017')
        self.db=self.client['UserData']
        self.admindata=self.db['admin']        
        self.superuserdata=self.db['superuser']
        self.userdata=self.db['user']

    def superuser(self,username,password):
        data=self.superuserdata.find_one({'username':username, 'password':password})
        print("superuser Verified")
        return data

    def admin(self,username,password):
        data=self.admindata.find_one({'username':username, 'password':password})
        return data
    
    def user(self,username,password,department):
        print(username,password,department)
        data=self.userdata.find_one({'username':username,'password':password,'department':department})
        department_admin=self.admindata.find_one({'department':department})
        department_admin=department_admin['username']
        print(data)
        return data,department_admin

    
    def verify_user(self,username,role):
        if role=='superuser':
            print('Superuser role verified')
            data=self.superuserdata.find({'username':username})
            return data
        if role=='admin':
            print('Admin role verified')
            data=self.admindata.find({'username':username})
            return data
        if role=='user':
            data=self.userdata.find({'username':username})
            return data



    def superuserdetails(self):
        admindata=self.admindata.count_documents({})
        userdata=self.userdata.count_documents({})
        return admindata,userdata
    
    def userdetails(self,department):
        print(department)
        userdata=self.userdata.count_documents({'department':department})
        return userdata

    def createadmin(self,username,password,department):
        self.admindata.insert_one({'username':username, 'password':password,'role':'admin','department':department})
        return 'sucessfully created admin'
    
    def createuser(self,username,password,department):
        self.userdata.insert_one({'username':username, 'password':password,'role':'user','department':department})
        return 'sucessfully created user'

  
            

        