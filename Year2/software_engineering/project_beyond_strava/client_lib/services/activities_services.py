from ..client import APIClient

client = APIClient()

def get_activity(activity_id):
    return client.get(f"/activities/{activity_id}")

def get_all_activities():
    return client.get("/activities")

def add_activity(activity_data):
    return client.post("/activities", data=activity_data)

def update_activity(activity_id, update_data):
    return client.put(f"/activities/{activity_id}", data=update_data)

def delete_activity(activity_id):
    return client.delete(f"/activities/{activity_id}")