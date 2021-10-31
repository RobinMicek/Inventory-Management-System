from pymongo import MongoClient
import pymongo

from datetime import datetime

#Current date and time
date_and_time = datetime.today().strftime("%d.%m.%y - %H:%M:%S")

#DB Connection init
client = MongoClient()
db = client.InventoryManagementSystem

#Tables
users = db.Users
items = db.Items



#User auth
class User():
    def __init__(self, username):
        self.username = username

        self.query = users.find_one({"username": str(self.username)})

    def new_user(self, pin):
        #Check if user exists
        if users.find_one({"username": str(self.username)})==None and users.find_one({"pin": int(pin)})==None:
            #Create user
            users.insert_one({
                "username": str(self.username),
                "pin": int(pin)
            })

            return True


    def login(self, pin):
        usr = users.find_one({
            "username": str(self.username)
        })        

        if usr != None:
            if usr["pin"] == int(pin):
                return True


#Item handeling
class Item():
    def __init__(self, code):
        self.code = code

        self.query = items.find_one({"code": str(self.code)})


    def add_new_item(self, Name, Location, Tag, Description):
        if self.query == None:
            items.insert_one({
                "code": str(self.code),
                "name": str(Name),
                "tag": str(Tag),
                "description": str(Description),
                "location": str(Location),
                "date_of_change": str(date_and_time)

            })

            return True
        
    def change_item_location(self, Username):
        if self.query != None:
            items.update_one(
                {"code": str(self.code)},
                {"$set": {
                    "location": str(Username),
                    "date_of_change": str(date_and_time)
                    }})
            
            return True


#Check if Users table is empty - For when running on different database host
def db_check():
    if users.count() == 0:
        users.insert_one({
                "username": "admin",
                "pin": int(1111)
            })

        print("""
        \n Created default credentials: \n
        Username: admin
        Pin: 1111 \n
        """)
