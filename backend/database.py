from pymongo import MongoClient

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# create/use database
db = client["smart_room"]

# create/use collection
collection = db["motion_events"]

def save_event(data):
    collection.insert_one(data)