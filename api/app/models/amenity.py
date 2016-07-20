import base
from peewee import *

class Amenity(base.BaseModel):
    name = CharField(null=False, max_length=128)

    def to_hash(self):
        values = {
            'name': self.name
        }
        return super(Amenity, self).to_hash(values)

