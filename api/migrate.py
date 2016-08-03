from app.models.base import db
from app.models.user import User
from app.models.state import State
from app.models.city import City
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities

from app.models.review import Review
from app.models.review_place import ReviewPlace
from app.models.review_user import ReviewUser


'''create tables'''
db.connect()
db.create_tables([User, State, City, Place, PlaceBook, Amenity, PlaceAmenities, Review, ReviewPlace, ReviewUser], safe = True)
db.close()
