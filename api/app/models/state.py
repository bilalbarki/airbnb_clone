import base
from peewee import *

class State(base.BaseModel):
    name = CharField(null=False, unique=True, max_length=128)
