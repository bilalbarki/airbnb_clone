from peewee import *
from user import User
from base import db
from review import Review

'''Many to many relation for review and user'''
class ReviewUser(Model):
    user = ForeignKeyField(rel_model=User)
    review = ForeignKeyField(related_name="reviews_user", rel_model=Review)

    class Meta:
        database = db
