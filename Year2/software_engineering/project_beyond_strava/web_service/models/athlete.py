from mongoengine import DynamicDocument, StringField, IntField, BooleanField, FloatField, DateTimeField, URLField

class Athlete(DynamicDocument):
    # ─── Identification ───────────────────────────────────────────────────────────
    athlete_id = IntField()
    #id         = StringField()
    username  = StringField(required=True)

    # ─── Personal Information ─────────────────────────────────────────────────────
    firstname = StringField(required=True, max_length=100)
    lastname  = StringField(required=True, max_length=100)
    sex       = StringField(choices=('M', 'F', 'O'), default='O')
    weight    = FloatField(min_value=0, default=0.0)

    # ─── Location ─────────────────────────────────────────────────────────────────
    city      = StringField(default='')
    state     = StringField(default='')
    country   = StringField(default='')

    #the following fields are present in the db but are not important for our API
    #badge_type_id = IntField()
    #bio = StringField()
    #created_at = DateTimeField()
    #premium = BooleanField()
    #profile = URLField()
    #profile_medium = URLField()
    #resource_state = IntField()
    #summit = BooleanField()
    #updated_at = DateTimeField()

    meta = {
        'collection': 'athletes'
    }
