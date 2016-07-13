import base
from user import User
from state import State
from city import City
from place import Place
from place_book import PlaceBook
from amenity import Amenity
from place_amenity import PlaceAmenities
from peewee import *

base.db.connect()
base.db.create_tables([User, State, City, Place, PlaceBook, Amenity, PlaceAmenities], safe = True)
base.db.close()
