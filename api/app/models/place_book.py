import base
from peewee import *
from place import *
from user import *

'''defines table for place bookings'''
class PlaceBook(base.BaseModel):
    place = ForeignKeyField(rel_model=Place)
    user = ForeignKeyField(related_name="places_booked", rel_model=User)
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False, formats="%Y/%m/%d %H:%M:%S")
    number_nights = IntegerField(default=1)

    '''returns placebook row as a dict'''
    def to_dict(self):
        place_book_dict = super(PlaceBook, self).to_dict()

        place_book_dict.update({
            'place_id': self.place.id,
            'user_id': self.user.id,
            'is_validated': self.is_validated,
            'date_start': self.date_start.strftime("%Y/%m/%d %H:%M:%S"),
            'number_nights': self.number_nights
        })
        return place_book_dict
