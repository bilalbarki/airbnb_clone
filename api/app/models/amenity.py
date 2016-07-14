import base
from peewee import *

class Amenity(base.BaseModel):
    name = CharField(null=False, max_length=128)

    def to_hash(self):
        data = {}
        data['name'] = self.name
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['id'] = self.id
        return data
