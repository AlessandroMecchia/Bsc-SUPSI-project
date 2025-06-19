from client_lib import *
import matplotlib.pyplot as plt
import polyline
import folium

def get_activities_by_athlete_id(athlete_id):
    all_activities = get_all_activities()  # Your existing function that fetches all activities
    return [activity for activity in all_activities if activity.get('athlete_id') == athlete_id]

def compare_athletes():
    print("\n>> Compare Two Athletes in a Sport")

    # Input ID primo atleta
    try:
        athlete1_id = int(input("Enter first athlete ID (integer): "))
    except ValueError:
        print("Invalid input. Athlete ID must be an integer.")
        return

    # Input ID secondo atleta
    try:
        athlete2_id = int(input("Enter second athlete ID (integer): "))
    except ValueError:
        print("Invalid input. Athlete ID must be an integer.")
        return

    # Scegli sport
    sports_choices = ['Run', 'Swim', 'Ride']
    print("Choose sport from:", sports_choices)
    sport = input("Enter sport: ").strip()
    if sport not in sports_choices:
        print("Invalid sport choice.")
        return

    # Recupera attività per entrambi gli atleti
    activities1 = get_activities_by_athlete_id(athlete1_id)
    activities2 = get_activities_by_athlete_id(athlete2_id)

    # Filtra attività per lo sport scelto
    filtered1 = [a for a in activities1 if a.get('sport_type') == sport]
    filtered2 = [a for a in activities2 if a.get('sport_type') == sport]

    # Controlla se entrambi hanno attività nello sport
    if not filtered1:
        print(f"Athlete {athlete1_id} has no activities in {sport}. Cannot compare.")
        return
    if not filtered2:
        print(f"Athlete {athlete2_id} has no activities in {sport}. Cannot compare.")
        return

    # Calcola statistiche per atleta 1
    dist1 = sum(a.get('distance', 0) for a in filtered1)
    elev1 = sum(a.get('total_elevation_gain', 0) for a in filtered1)
    count1 = len(filtered1)

    # Calcola statistiche per atleta 2
    dist2 = sum(a.get('distance', 0) for a in filtered2)
    elev2 = sum(a.get('total_elevation_gain', 0) for a in filtered2)
    count2 = len(filtered2)

    # Stampa confronto
    print(f"\nComparison in {sport} between Athlete {athlete1_id} and Athlete {athlete2_id}:")
    print(f"Athlete {athlete1_id}: {dist1 / 1000:.2f} km, {elev1:.2f} m elevation, {count1} activities")
    print(f"Athlete {athlete2_id}: {dist2 / 1000:.2f} km, {elev2:.2f} m elevation, {count2} activities")


def aggregate_athlete_stats(activities):
    total_distance = sum(a.get('distance', 0) for a in activities) / 1000  # meters to km
    total_elevation_gain = sum(a.get('total_elevation_gain', 0) for a in activities)
    total_activities = len(activities)
    avg_speed = (sum(a.get('average_speed', 0) for a in activities) / total_activities) * 3.6 if total_activities else 0  # m/s to km/h
    heartrates = [a.get('average_heartrate') for a in activities if a.get('average_heartrate') is not None]
    avg_heartrate = sum(heartrates) / len(heartrates) if heartrates else 0
    return {
        'total_distance': total_distance,
        'total_elevation_gain': total_elevation_gain,
        'total_activities': total_activities,
        'avg_speed': avg_speed,
        'avg_heartrate': avg_heartrate,
    }

def list_athlete_activities():
    print("\n>> List Athlete's Activities")
    try:
        athlete_id = int(input("Enter athlete ID (integer): "))
    except ValueError:
        print("Invalid input. Athlete ID must be an integer.")
        return

    activities = get_activities_by_athlete_id(athlete_id)
    if not activities:
        print("No activities found for this athlete.")
        return

    print(f"Activities for athlete ID {athlete_id}:")
    for a in activities:
        distance_km = a.get('distance', 0) / 1000
        print(f"- ID: {a.get('id')} | Name: {a.get('name')} | Sport: {a.get('sport_type')} | Distance: {distance_km:.2f} km | Moving time: {a.get('moving_time', 0)//60} min")


def athlete_statistics_overview():
    print("\n>> Athlete Statistics Overview")
    try:
        athlete_id = int(input("Enter athlete ID (integer): "))
    except ValueError:
        print("Invalid input. Athlete ID must be an integer.")
        return

    activities = get_activities_by_athlete_id(athlete_id)
    if not activities:
        print("No activities found for this athlete.")
        return

    stats_by_sport = {}
    for a in activities:
        sport = a.get('sport_type', 'Unknown')
        if sport not in stats_by_sport:
            stats_by_sport[sport] = {'distance': 0, 'elevation_gain': 0, 'count': 0}
        stats_by_sport[sport]['distance'] += a.get('distance', 0)
        stats_by_sport[sport]['elevation_gain'] += a.get('total_elevation_gain', 0)
        stats_by_sport[sport]['count'] += 1

    print(f"Statistics for athlete ID {athlete_id}:")
    for sport, stats in stats_by_sport.items():
        print(f"- {sport}:")
        print(f"  Total distance: {stats['distance']/1000:.2f} km")
        print(f"  Total elevation gain: {stats['elevation_gain']:.2f} m")
        print(f"  Total activities: {stats['count']}")


def visualize_routes_and_streams():
    print("\n>> Visualize Routes and Streams")
    try:
        athlete_id = int(input("Enter athlete ID (integer): "))
    except ValueError:
        print("Invalid input. Athlete ID must be an integer.")
        return

    activities = get_activities_by_athlete_id(athlete_id)
    if not activities:
        print("No activities found for this athlete.")
        return

    # Filter only 'Run' activities that have valid polyline
    run_activities = [a for a in activities if a.get('sport_type') == 'Run' and a.get('map', {}).get('summary_polyline')]

    if not run_activities:
        print("No running activities with map data found for this athlete.")
        return

    # Initialize map centered at first run's start location
    first_coords = polyline.decode(run_activities[0]['map']['summary_polyline'])
    if not first_coords:
        print("Could not decode polyline for the first activity.")
        return

    start_lat, start_lon = first_coords[0]
    route_map = folium.Map(location=[start_lat, start_lon], zoom_start=13)

    # Add all run routes as polylines with different colors
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 'lightblue', 'lightgreen']
    for i, activity in enumerate(run_activities):
        coords = polyline.decode(activity['map']['summary_polyline'])
        folium.PolyLine(coords, color=colors[i % len(colors)], weight=4, opacity=0.7,
                        tooltip=f"{activity.get('name', 'Run')} ({activity.get('distance', 0)/1000:.2f} km)").add_to(route_map)

    filename = f"all_runs_athlete_{athlete_id}.html"
    route_map.save(filename)
    print(f"Map with all runs saved as {filename}")
