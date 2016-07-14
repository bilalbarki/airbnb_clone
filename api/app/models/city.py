import base
from peewee import *
from state import *
from playhouse.shortcuts import model_to_dict

class City(base.BaseModel):
    name = CharField(null=False, max_length=128)
    state = ForeignKeyField(related_name="cities", rel_model=State, on_delete='CASCADE')

    def to_hash(self):
        query = City.select(City.id, City.created_at, City.updated_at, City.name, City.state_id).get()
        return model_to_dict(query)
