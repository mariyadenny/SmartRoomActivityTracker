from pymongo import MongoClient

def get_collection():
    client = MongoClient("localhost", 27017)
    db = client["smart_room_db"]
    return db["motion_events"]

def insert_motion_event(event):
    collection = get_collection()
    return collection.insert_one(event)