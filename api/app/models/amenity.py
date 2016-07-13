import base
from peewee import *

class Amenity(base.BaseModel):
    name = CharField(null=False, max_length=128)
