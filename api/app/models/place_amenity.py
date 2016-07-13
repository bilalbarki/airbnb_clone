from peewee import *
from place import *
from amenity import *
import base

class PlaceAmenities(Model):
    place = ForeignKeyField(rel_model=Place)
    amenity = ForeignKeyField(rel_model=Amenity)

    class Meta:
        database = base.db
