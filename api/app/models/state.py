import base
from peewee import *
from playhouse.shortcuts import model_to_dict

class State(base.BaseModel):
    name = CharField(null=False, unique=True, max_length=128)

    def to_hash(self):
        values = {
            "name":self.name
        }
        return super(State, self).to_hash(values)
