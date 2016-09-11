import base
from peewee import *
from state import *

'''defines table for cities'''
class City(base.BaseModel):
    name = CharField(null=False, max_length=128)
    state = ForeignKeyField(related_name="cities", rel_model=State, on_delete='CASCADE')

    '''returns row of city as a dict'''
    def to_dict(self):
    	city_dict = super(City, self).to_dict()
        
        city_dict.update({
            "name": self.name,
            "state_id": self.state.id
        })
        return city_dict
