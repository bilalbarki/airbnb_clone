import base
from peewee import *
from state import *
from playhouse.shortcuts import model_to_dict

class City(base.BaseModel):
    name = CharField(null=False, max_length=128)
    state = ForeignKeyField(related_name="cities", rel_model=State, on_delete='CASCADE')

    def to_hash(self):
        state = State.get(State.id == self.state)
        values = {
            "name":self.name,
            "state_id":state.id
        }
        return super(City, self).to_hash(values)
