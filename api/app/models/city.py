import base
from peewee import *
from state import *
from playhouse.shortcuts import model_to_dict

class City(base.BaseModel):
    name = CharField(null=False, max_length=128)
    state = ForeignKeyField(related_name="cities", rel_model=State, on_delete='CASCADE')

    def to_hash(self):
        values = {"id":self.id,"created_at":self.created_at,"updated_at":self.updated_at,"name":self.name}
        return values
