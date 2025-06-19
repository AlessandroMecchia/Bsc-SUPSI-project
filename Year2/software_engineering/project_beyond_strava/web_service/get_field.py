from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_url = os.getenv("MONGO_URL")

client = MongoClient(mongo_url)
db = client["strava_db"]
collection = db["athletes"]
collection = db["activites"]#to correct in db in activities

fields = set()

for doc in collection.find():
    fields.update(doc.keys())

print("All fields in 'activites' collection:")
for field in sorted(fields):
    print(f"- {field}")
