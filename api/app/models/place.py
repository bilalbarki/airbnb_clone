import base
from peewee import *
from user import *
from city import *

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

    def to_dict(self):
        place_dict = super(Place, self).to_dict()
        # t = (City.id == self.city) & (User.id == self.owner)
        # query = City.select(City, User).join(User, on=t).get()
        #city = City.get(City.id == self.city)
        #owner = User.get(User.id == self.owner)
        
        place_dict.update({
            'number_bathrooms': self.number_bathrooms,
            'max_guest': self.max_guest,
            'price_by_night': self.price_by_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'city_id': self.city.id,
            'name': self.name,
            'description': self.description,
            'number_rooms': self.number_rooms
        })
        return place_dict
