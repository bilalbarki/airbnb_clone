from peewee import *
from user import User
from base import db
from place import Place
from review import Review

class ReviewPlace(Model):
    place = ForeignKeyField(rel_model=Place)
    review = ForeignKeyField(rel_model=Review)

    class Meta:
        database = db
