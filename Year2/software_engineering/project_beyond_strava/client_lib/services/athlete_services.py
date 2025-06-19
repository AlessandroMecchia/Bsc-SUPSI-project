from ..client import APIClient

client = APIClient()

def get_athlete(athlete_id):
    return client.get(f"/athletes/{athlete_id}")

def get_all_athletes():
    return client.get("/athletes")

def add_athlete(athlete_data):
    return client.post("/athletes", data=athlete_data)

def update_athlete(athlete_id, update_data):
    return client.put(f"/athletes/{athlete_id}", data=update_data)

def delete_athlete(athlete_id):
    return client.delete(f"/athletes/{athlete_id}")

def get_summary_athlete(athlete_id):
    return client.get(f"/athletes/{athlete_id}/summary")


