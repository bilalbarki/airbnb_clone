import base
from peewee import *
from playhouse.shortcuts import model_to_dict

class State(base.BaseModel):
    name = CharField(null=False, unique=True, max_length=128)

    def to_dict(self):
        state_dict = super(State, self).to_dict()
       	state_dict.update({
            "name": self.name
       	})
        return state_dict
