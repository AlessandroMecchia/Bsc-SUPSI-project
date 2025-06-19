from mongoengine.errors import DoesNotExist
from web_service.models.athlete import Athlete
from web_service.models.activity import Activity

def format_pace(pace_min_per_km):
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}:{seconds:02d} /km"

def get_athlete_summary(athlete_id):
    try:
        athlete = Athlete.objects.get(athlete_id=athlete_id)
    except DoesNotExist:
        return None

    qs = Activity.objects(athlete_id=athlete_id)

    total_activities   = qs.count()
    total_distance = (qs.sum('distance') or 0) / 1000
    avg_speed          = qs.average('average_speed') or 0
    total_elevation    = qs.sum('total_elevation_gain') or 0
    avg_heartrate      = qs.average('average_heartrate') or None

    # Fix for max heartrate
    max_hr_doc = qs.order_by('-max_heartrate').first()
    max_heartrate = max_hr_doc.max_heartrate if max_hr_doc and max_hr_doc.max_heartrate else None

    pace_min_per_km = 60 / (avg_speed * 3.6) if avg_speed > 0 else None
    avg_pace = format_pace(pace_min_per_km) if pace_min_per_km else None

    return {
        'athlete_id':        athlete_id,
        'total_activities':  total_activities,
        'total_distance':    round(total_distance, 1),
        'total_elevation':   round(total_elevation, 1),
        'average_speed':     round(avg_speed, 2),
        'average_pace':      avg_pace,
        'average_heartrate': round(avg_heartrate, 1) if avg_heartrate else None,
        'max_heartrate':     round(max_heartrate, 1) if max_heartrate else None,
    }

