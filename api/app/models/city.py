import base
from peewee import *
from state import *
from playhouse.shortcuts import model_to_dict

class City(base.BaseModel):
    name = CharField(null=False, max_length=128)
    state = ForeignKeyField(related_name="cities", rel_model=State, on_delete='CASCADE')

    def to_dict(self):
    	city_dict = super(City, self).to_dict()
        #state = State.get(State.id == self.state)
        
        city_dict.update({
            "name": self.name,
            "state_id": self.state.id
        })
        return city_dict
