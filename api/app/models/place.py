import base
from peewee import *
from user import *
from city import *
from playhouse.shortcuts import model_to_dict

class Place(base.BaseModel):
    owner = ForeignKeyField(related_name="places", rel_model=User)
    city = ForeignKeyField(related_name="places", rel_model=City)
    name = CharField(null=False, max_length=128)
    description = TextField()
    number_rooms = IntegerField(default=0)
    number_bathrooms = IntegerField(default=0)
    max_guest = IntegerField(default=0)
    price_by_night = IntegerField(default=0)
    latitude = FloatField()
    longitude = FloatField()

    '''def to_hash(self):
        query = Place.select(Place.id, Place.created_at, Place.updated_at, Place.).get()
        return model_to_dict(query)'''
