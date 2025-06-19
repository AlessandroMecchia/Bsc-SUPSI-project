from client_lib import *
from fitparse import FitFile
import uuid
import matplotlib.pyplot as plt
import folium
import polyline
import random

def view_id_activities():
    activities = get_all_activities()
    for activity in activities:
        print(f"ID: {activity['id']} - Name: {activity['name']} - Type:{activity['type']}")


def extract_all_fit_data(file_path, athlete_id):
    fitfile = FitFile(file_path)
    random_id = random.randint(10000_000_000, 99999999999)
    id = uuid.uuid4().int % (1 << 63)
    data = {
        "achievement_count": 0,
        "athlete": {
            "id": athlete_id,
            "resource_state": 1
        },
        "athlete_count": 1,
        "athlete_id": athlete_id,
        "comment_count": 0,
        "commute": False,
        "device_watts": False,
        "display_hide_heartrate_option": True,
        "id": random_id,  # unique ID
        "flagged": False,
        "from_accepted_tag": False,
        "gear_id": None,
        "has_heartrate": False,
        "has_kudoed": False,
        "heartrate_opt_out": False,
        "kudos_count": 0,
        "location_city": None,
        "location_country": None,
        "location_state": None,
        "manual": False,
        "map": {
            "id": f"a{random_id}",
            "resource_state": 2,
            "summary_polyline": ""
        },
        "photo_count": 0,
        "pr_count": 0,
        "private": False,
        "resource_state": 2,
        "sport_type": "Run",  # fallback
        "start_latlng": None,  # default None, will set if valid
        "end_latlng": None,    # default None, will set if valid
        "streams": {},
        "suffer_score": 0.0,
        "timezone": "(GMT+02:00) Europe/Rome",
        "total_elevation_gain": 0.0,
        "total_photo_count": 0,
        "trainer": False,
        "type": "Run",
        "upload_id": int(uuid.uuid4().int >> 64),
        "upload_id_str": str(uuid.uuid4().int >> 64),
        "utc_offset": 7200.0,
        "visibility": "everyone"
    }

    speeds, heart_rates, distances, timestamps, elevations = [], [], [], [], []
    for record in fitfile.get_messages('record'):
        for record_data in record:
            name = record_data.name
            value = record_data.value
            if name == 'speed':
                speeds.append(value)
            elif name == 'heart_rate':
                heart_rates.append(value)
                data['has_heartrate'] = True
            elif name == 'distance':
                distances.append(value)
            elif name == 'timestamp':
                timestamps.append(value)
            elif name == 'enhanced_altitude':
                elevations.append(value)

    if speeds:
        data["average_speed"] = sum(speeds) / len(speeds)
        data["max_speed"] = max(speeds)
    if heart_rates:
        data["average_heartrate"] = sum(heart_rates) / len(heart_rates)
        data["max_heartrate"] = max(heart_rates)
    if distances:
        data["distance"] = max(distances)
    if elevations:
        data["elev_high"] = max(elevations)
        data["elev_low"] = min(elevations)
        data["total_elevation_gain"] = max(elevations) - min(elevations)
    if timestamps:
        data["elapsed_time"] = (max(timestamps) - min(timestamps)).total_seconds()
        data["moving_time"] = data["elapsed_time"]

        # Start date in ISO format
        data["start_date"] = timestamps[0].isoformat()
        data["start_date_local"] = timestamps[0].isoformat()

        # Compute relative times in seconds for streams
        start_time = timestamps[0]
        time_seconds = [(ts - start_time).total_seconds() for ts in timestamps]
    else:
        time_seconds = []

    # Fill streams
    data["streams"] = {
        "time": time_seconds,
        "heartrate": heart_rates,
        "speed": speeds,
        "distance": distances,
        "elevation": elevations,
    }

    # Generate start and end latlng from polyline if available and valid
    polyline_str = data["map"].get("summary_polyline")
    if polyline_str:
        coords = polyline.decode(polyline_str)
        if coords and len(coords) >= 2:
            data["start_latlng"] = {
                "type": "Point",
                "coordinates": [coords[0][1], coords[0][0]]  # Note: GeoJSON expects [lon, lat]
            }
            data["end_latlng"] = {
                "type": "Point",
                "coordinates": [coords[-1][1], coords[-1][0]]
            }

    # Sport type and name from 'sport' message if available
    for activity in fitfile.get_messages('sport'):
        for record_data in activity:
            if record_data.name == 'sport':
                data["type"] = record_data.value
                data["sport_type"] = record_data.value
                data["name"] = f"{record_data.value} Activity"
                break

    return data


def view_all_activities():
    activities = get_all_activities()
    if not activities:
        print("No activities found.")
        return
    for activity in activities:
        print(f"-------------------------------")
        print(f"Name: {activity.get('name', 'Unnamed')}")
        print(f"ID: {activity['id']}")
        print(f"Distance: {activity.get('distance', 0)} m")
        print(f"Elapsed Time: {activity.get('elapsed_time', 0)} sec")
        print(f"Sport Type: {activity.get('sport_type', 'N/A')}")
        print(f"-------------------------------\n")

def add_activity_interactive():
    print("\n>> Add Activity")
    athlete_id = input("Enter athlete ID to assign activity: ")
    athlete = get_athlete(athlete_id)
    if not athlete:
        print("Athlete not found. Cannot proceed.")
        return

    file_path = input("Enter path to FIT file: ").strip().strip('"').strip("'")
    activity_data = extract_all_fit_data(file_path, athlete['athlete_id'])
    if add_activity(activity_data):
        print(f"Activity '{activity_data.get('name', 'Unnamed')}' added for athlete {athlete['firstname']} {athlete['lastname']}")
    else:
        print("Failed to add activity.")

def edit_activity():
    print("\n>> Edit Activity")
    activity_id = input("Enter activity ID: ")

    activity = get_activity(activity_id)
    if not activity:
        print("Activity not found.")
        return

    update_data = {}

    new_name = input(f"New name (current: {activity.get('name', '')}, leave blank to keep current): ")
    if new_name:
        update_data['name'] = new_name

    new_description = input(f"New description (current: {activity.get('description', '')}, leave blank to keep current): ")
    if new_description:
        update_data['description'] = new_description

    if update_data:
        response = update_activity(activity_id, update_data)
        if response.status_code == 200:
            print("Activity updated successfully!")
        else:
            print(f"Failed to update activity: {response.status_code} - {response.text}")
    else:
        print("No changes made.")

def delete_old_activity():
    print("\n>> Delete Activity")
    activity_id = int(input("Enter activity ID: "))

    activity = get_activity(activity_id)
    if activity:
        confirm = input(f"Are you sure you want to delete activity '{activity['name']}'? (y/n): ")
        if confirm.lower() == 'y':
            response = delete_activity(activity_id)
            if response.status_code == 200:
                print("Activity deleted successfully!")
            else:
                print(f"Failed to delete activity: {response.status_code} - {response.text}")
        else:
            print("Deletion cancelled.")
    else:
        print("Activity not found.")

def show_activity_details():
    activity_id = input("Enter activity ID: ")
    activity = get_activity(activity_id)
    if not activity:
        print("Activity not found.")
        return

    print(f"Name: {activity.get('name', 'N/A')}")
    print(f"Sport type: {activity.get('sport_type', 'N/A')}")
    print(f"Distance: {activity.get('distance', 0) / 1000:.2f} km")
    print(f"Moving time: {activity.get('moving_time', 0) // 60} minutes")
    print(f"Average speed: {activity.get('average_speed', 0) * 3.6:.2f} km/h")
    print(f"Average heart rate: {activity.get('average_heartrate', 'N/A')}")
    print(f"Max heart rate: {activity.get('max_heartrate', 'N/A')}")
    print(f"Kudos: {activity.get('kudos_count', 0)}")
    print(f"Suffer score: {activity.get('suffer_score', 'N/A')}")

    streams = activity.get('streams', {})

    # Extract stream data
    time_stream = streams.get('time', {}).get('data', [])
    hr_stream = streams.get('heartrate', {}).get('data', [])
    speed_stream = streams.get('speed', {}).get('data', [])
    altitude_stream = streams.get('altitude', {}).get('data', [])

    # Plot heart rate
    if time_stream and hr_stream:
        plt.figure(figsize=(10, 3))
        plt.plot(time_stream, hr_stream, label='Heart Rate (bpm)')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Heart Rate (bpm)')
        plt.title(f"Heart Rate over Time - {activity.get('name')}")
        plt.legend()
        plt.grid(True)
        plt.show()

    # Plot speed
    distance_stream = streams.get('distance', {}).get('data', [])

    if time_stream and distance_stream and len(time_stream) == len(distance_stream):
        speed_stream = [0] + [
            (distance_stream[i] - distance_stream[i - 1]) / (time_stream[i] - time_stream[i - 1] or 1)
            for i in range(1, len(time_stream))
        ]

        pace_stream = [
            60 / (s * 3.6) if s > 0 else None
            for s in speed_stream
        ]

        filtered_time = [t for t, p in zip(time_stream, pace_stream) if p is not None]
        filtered_pace = [p for p in pace_stream if p is not None]

        plt.figure(figsize=(10, 3))
        plt.plot(filtered_time, filtered_pace, label='Pace (min/km)')
        plt.xlabel('Time (s)')
        plt.ylabel('Pace (min/km)')
        plt.title(f"Pace over Time - {activity.get('name')}")
        plt.gca().invert_yaxis()
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("Pace not available: missing or mismatched distance/time data.")

    # Plot altitude
    if time_stream and altitude_stream:
        plt.figure(figsize=(10, 3))
        plt.plot(time_stream, altitude_stream, label='Altitude (m)')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Altitude (meters)')
        plt.title(f"Altitude over Time - {activity.get('name')}")
        plt.legend()
        plt.grid(True)
        plt.show()

    # Plot route on a map
    polyline_str = activity.get('map', {}).get('summary_polyline')
    if polyline_str:
        coords = polyline.decode(polyline_str)  # list of (lat, lon)
        if coords:
            start_lat, start_lon = coords[0]
            route_map = folium.Map(location=[start_lat, start_lon], zoom_start=14)
            folium.PolyLine(coords, color='blue', weight=5).add_to(route_map)
            # Display map in a Jupyter notebook or save to HTML:
            route_map.save("route_map.html")
            print("Route map saved to route_map_specific_activity.html")
        else:
            print("No coordinates decoded from polyline.")
    else:
        print("No map polyline available for this activity.")