import base
from peewee import *
from user import *
from city import *
from playhouse.shortcuts import model_to_dict

class Place(base.BaseModel):
    owner = ForeignKeyField(related_name="places", rel_model=User)
    city = ForeignKeyField(related_name="places", rel_model=City)
    name = CharField(null=False, max_length=128)
    description = TextField()
    number_rooms = IntegerField(default=0)
    number_bathrooms = IntegerField(default=0)
    max_guest = IntegerField(default=0)
    price_by_night = IntegerField(default=0)
    latitude = FloatField()
    longitude = FloatField()

    def to_hash(self):
        quert = {}
        city = City.get(City.id == self.city)
        owner = User.get(User.id == self.owner)
        
        query['number_bathrooms'] = self.number_bathrooms
        query['max_guest'] = self.max_guest
        query['price_by_night'] = self.price_by_night
        query['latitude'] = self.latitude
        query['longitude'] = self.longitude
        query['owner_id'] = owner.id
        query['city_id'] = city.id
        query['name'] = self.name
        query['description'] = self.description
        query['number_rooms'] = self.number_rooms
        query['created_at'] = self.created_at
        query['updated'] = self.updated_at
        return query
