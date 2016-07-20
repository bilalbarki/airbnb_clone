import base
from peewee import *
from place import *
from user import *

class PlaceBook(base.BaseModel):
    place = ForeignKeyField(rel_model=Place)
    user = ForeignKeyField(related_name="places_booked", rel_model=User)
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False, formats="%Y/%m/%d %H:%M:%S")
    number_nights = IntegerField(default=1)

    def to_hash(self):
        place = Place.get(Place.id == self.place)
        user = User.get(User.id == self.user)
        values = {
            'place_id': place.id,
            'user_id': user.id,
            'is_validated': self.is_validated,
            'user_id': user.id,
            'is_validated': self.is_validated,
            'date_start': self.date_start.strftime("%Y/%m/%d %H:%M:%S"),
            'number_nights': self.number_nights
        }
        return super(PlaceBook, self).to_hash(values)
