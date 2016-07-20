from app.models.base import db
from app.models.user import User
from app.models.state import State
from app.models.city import City
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities

'''create tables'''
db.connect()
db.create_tables([User, State, City, Place, PlaceBook, Amenity, PlaceAmenities], safe = True)
db.close()
