from pymongo import MongoClient

# connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# select database
db = client["smart_room"]

# select collection (like a table)
collection = db["motion_events"]

# save one motion event to DB
def save_event(data):
    collection.insert_one(data)

# get all events (sorted by newest first)
def get_all_events():
    events = list(collection.find({}, {"_id": 0}).sort("received_at_utc", -1))
    return events

# count total number of events
def get_event_count():
    return collection.count_documents({})