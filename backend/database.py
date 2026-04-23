from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["smart_room"]
collection = db["motion_events"]

def save_event(data):
    collection.insert_one(data)

def get_all_events():
    events = list(collection.find({}, {"_id": 0}).sort("received_at_utc", -1))
    return events

def get_event_count():
    return collection.count_documents({})