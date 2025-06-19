from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests

load_dotenv()

mongo_url = os.getenv('MONGO_URL')
strava_access_token = os.getenv('STRAVA_ACCESS_TOKEN')
client = MongoClient(mongo_url)

db = client['strava_db']

activities_collection = db['activities']
athletes_collection = db['athletes']


# deprecated
# headers = {'access_token' : strava_access_token}
headers = {"Authorization": f"Bearer {strava_access_token}"}

response_all_activities = requests.get('https://www.strava.com/api/v3/athlete/activities', headers=headers)

if response_all_activities.status_code == 200:
    activities = response_all_activities.json()

    # add the activity if it doesn't exist
    for activity in activities:
        activity_id = activity['id']

        existing_activity = activities_collection.find_one({"id": activity_id})

        if not existing_activity:
            # link the activity to the athlete
            activity['athlete_id'] = activity['athlete']['id']
            
            if activity['type'] == 'Run':

                streams_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams"
                params = {
                    'keys': 'latlng,time,heartrate,altitude',
                    'key_by_type': 'true'
                }
                streams_response = requests.get(streams_url, headers=headers, params=params)

                if streams_response.status_code == 200:
                    streams_data = streams_response.json()
                    activity['streams'] = streams_data
                    print(f"Added streams for activity {activity_id}")
                else:
                    print(f"Failed to fetch streams for activity {activity_id}")

            activities_collection.insert_one(activity)

else:
    print(f"Error API for activity {response_all_activities.status_code}")

response_athlete = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)

if response_athlete.status_code == 200:
    athlete = response_athlete.json()

    athlete['athlete_id'] = athlete['id']

    if 'id' in athlete:
        del athlete['id']
        
    existing_athlete = athletes_collection.find_one({"athlete_id": athlete['athlete_id']})

    if not existing_athlete:
        athletes_collection.insert_one(athlete)
        print(f"Saved athlete {athlete['athlete_id']}")
    else:
        print(f"Athlete {athlete['athlete_id']} already exists")
else:
    
    print(f"Error API for athlete: {response_athlete.status_code}")
    print("Response body:", response_athlete.text)
