import base
from peewee import *

'''defines amenity table'''
class Amenity(base.BaseModel):
    name = CharField(null=False, max_length=128)

    '''returns row of amenity as a dict'''
    def to_dict(self):
    	amenity_dict = super(Amenity, self).to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict

