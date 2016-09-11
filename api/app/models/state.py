import base
from peewee import *

'''defines State'''
class State(base.BaseModel):
    name = CharField(null=False, unique=True, max_length=128)

    '''returns row of state in a dict'''
    def to_dict(self):
        state_dict = super(State, self).to_dict()
       	state_dict.update({
            "name": self.name
       	})
        return state_dict
