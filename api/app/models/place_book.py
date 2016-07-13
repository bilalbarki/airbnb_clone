import base
from peewee import *
from place import *
from user import *

class PlaceBook(base.BaseModel):
    place = ForeignKeyField(rel_model=Place)
    user = ForeignKeyField(related_name="places_booked", rel_model=User)
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False)
    number_nights = IntegerField(default=1)
