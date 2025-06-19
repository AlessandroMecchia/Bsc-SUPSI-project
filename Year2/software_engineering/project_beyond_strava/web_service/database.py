from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url = os.getenv('MONGO_URL')

# Connect to MongoDB with MongoEngine
connect(
    db='strava_db',
    host=mongo_url,
    alias='default',
    uuidRepresentation='standard'  # This silences a warning 
)