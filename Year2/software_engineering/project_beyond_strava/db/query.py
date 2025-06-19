from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests

load_dotenv()

mongo_url = os.getenv('MONGO_URL')

client = MongoClient(mongo_url)

db = client['strava_db']

activities_collection = db['activites']
athletes_collection = db['athletes']

def find_athletes():
    athletes = list(athletes_collection.find())
    return athletes['_id']


if __name__ == "__main__":
    athletes = find_athletes()
    print(athletes)