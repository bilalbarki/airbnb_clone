from peewee import *
from place import *
from amenity import *
from base import db

class PlaceAmenities(Model):
    place = ForeignKeyField(rel_model=Place)
    amenity = ForeignKeyField(rel_model=Amenity)

    class Meta:
        database = db
