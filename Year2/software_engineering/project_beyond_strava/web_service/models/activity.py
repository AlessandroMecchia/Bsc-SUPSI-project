from web_service.models.athlete import Athlete
from mongoengine import (
    DynamicDocument, IntField, FloatField, StringField, BooleanField,
    DateTimeField, DictField, PointField, ReferenceField, ListField, EmbeddedDocumentField, EmbeddedDocument
)

class Activity(DynamicDocument):
    # ─── Identification ───────────────────────────────────────────────────────────
    #activity_id          = IntField(primary_key=True)
    _id                   = IntField(primary_key=True)
    id                    = IntField()
    #athlete_id           = IntField()
    athlete              = ReferenceField(Athlete, required=True)
    name                 = StringField(required=True, max_length=200)

    # ─── Timing ───────────────────────────────────────────────────────────────────
    start_date           = DateTimeField(required=True)
    start_date_local     = DateTimeField()
    timezone             = StringField()
    utc_offset           = FloatField()
    resource_state       = IntField(choices=(1,2,3), default=2)

    # ─── Location ─────────────────────────────────────────────────────────────────
    start_latlng         = PointField()   # [lng, lat]
    end_latlng           = PointField()

    # ─── Activity Meta ────────────────────────────────────────────────────────────
    activity_type        = StringField()
    sport_type           = StringField()
    commute              = BooleanField(default=False) # non-training trips
    device_watts         = BooleanField(default=False) # whether power came from device

    # ─── Time & Distance ─────────────────────────────────────────────────────────
    elapsed_time         = IntField()    
    moving_time          = IntField()    
    distance             = FloatField()   

    # ─── Speed & Cadence ─────────────────────────────────────────────────────────
    average_speed        = FloatField()   
    max_speed            = FloatField()   
    average_cadence      = FloatField()   

    # ─── Heart Rate ──────────────────────────────────────────────────────────────
    has_heartrate        = BooleanField(default=False)
    average_heartrate    = FloatField()   
    max_heartrate        = FloatField()  

    # ─── Power & Effort ──────────────────────────────────────────────────────────
    average_watts        = FloatField()   
    weighted_average_watts = IntField()  
    max_watts            = IntField()     
    kilojoules           = FloatField()   
    suffer_score         = FloatField()   

    # ─── Elevation ──────────────────────────────────────────────────────────────
    total_elevation_gain = FloatField()   # meters climbed
    elev_high            = FloatField()   # max elevation
    elev_low             = FloatField()   # min elevation

    # ─── Map & Streams ───────────────────────────────────────────────────────────
    map                  = DictField()    # {id, resource_state, summary_polyline}
    streams              = DictField()    # time series: latlng, heartrate, watts, etc.


    #the following fields are present in the db but are not important for our API

    #achievement_count = IntField()
    #athlete = DictField()  # Use ReferenceField(Athlete) if linking to Athlete model
    #athlete_count = IntField()
    #comment_count = IntField()
    #display_hide_heartrate_option = BooleanField()
    #external_id = StringField() # id to match external device
    # flagged = BooleanField() #flagged for suspicious data
    #from_accepted_tag = BooleanField()
    #gear_id = StringField()
    #has_kudoed = BooleanField()
    #heartrate_opt_out = BooleanField()
    #kudos_count = IntField()
    #location_city = StringField() #no data with api
    #location_country = StringField()
    #location_state = StringField()
    #manual = BooleanField() #activity inserted manually? less data
    #photo_count = IntField()
    #pr_count = IntField()
    #private = BooleanField()
    #total_photo_count = IntField()
    #trainer = BooleanField()
    #upload_id = IntField()
    #upload_id_str = StringField()
    #visibility = StringField()
    #workout_type = IntField()

    meta = {
        'collection': 'activities', 
        'indexes': ['start_date']
    }
