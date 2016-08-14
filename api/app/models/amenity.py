import base
from peewee import *

class Amenity(base.BaseModel):
    name = CharField(null=False, max_length=128)

    def to_dict(self):
    	amenity_dict = super(Amenity, self).to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict

