import base
from peewee import *
from playhouse.shortcuts import model_to_dict

class State(base.BaseModel):
    name = CharField(null=False, unique=True, max_length=128)

    def to_hash(self):
        values = {"id":self.id,"created_at":self.created_at,"updated_at":self.updated_at,"name":self.name}
        return values
