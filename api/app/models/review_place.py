from peewee import *
from user import User
from base import db
from place import Place
from review import Review

'''many to many relation between place and review'''
class ReviewPlace(Model):
    place = ForeignKeyField(rel_model=Place)
    review = ForeignKeyField(rel_model=Review)

    class Meta:
        database = db
