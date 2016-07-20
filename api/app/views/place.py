from flask import request, jsonify
from app import app
from app.models.city import City
from app.models.state import State
from app.models.place import Place
from app.models.place_book import PlaceBook
from flask_json import as_json

app.config['JSON_ADD_STATUS'] = False

@app.route('/places', methods=['GET'])
def get_places():
        places = []
        query = Place.select()
        for place in query:
            places.append(place.to_hash())
        return jsonify(places)

@app.route('/places', methods=['POST'])
@as_json
def create_new_place():
    post_data = request.values
    try:
        new_place = Place.create(
                owner = int(post_data['owner_id']),
                name = post_data['name'],
                city = int(post_data['city_id']),
                description = post_data['description'],
                latitude = float(post_data['latitude']),
                longitude = float(post_data['longitude'])
        )
    except:
        return {"code":404, "msg":"Parameters not correct"}
    if 'number_rooms' in post_data:
        new_place.number_rooms = int(post_data['number_rooms'])
    if 'number_bathrooms' in post_data:
        new_place.number_bathrooms = int(post_data['number_bathrooms'])
    if 'max_guest' in post_data:
        new_place.max_guest = int(post_data['max_guest'])
    if 'price_by_night' in post_data:
        new_place.price_by_night = int(post_data['price_by_night'])
    new_place.save()
    return new_place.to_hash()

@app.route('/places/<int:place_id>', methods=['GET', 'DELETE'])
@as_json
def place(place_id):
    if request.method == 'GET':
        try:
            new_place = Place.get(Place.id == place_id)
            return new_place.to_hash()
        except:
            return {'code':404, "msg":"not found"}
    else:
        query = Place.get(Place.id == place_id)
        out_dict = query.to_hash()
        query.delete_instance()
        return out_dict

@app.route('/places/<int:place_id>', methods=['PUT'])
@as_json
def put_place(place_id):
    post_data = request.values
    try:
        place = Place.get(Place.id == place_id)
    except:
        return {"code":404, "msg":"not found"}
    try:
        for key in post_data:
            if key == 'name':
                place.name = post_data[key]
            if key == 'description':
                place.description = post_data[key]
            if key == 'number_rooms':
                place.number_rooms = post_data[key]
            if key == 'number_bathrooms':
                place.number_bathrooms = post_data[key]
            if key == 'max_guest':
                place.max_guest = post_data[key]
            if key == 'price_by_night':
                place.price_by_night = post_data[key]
            if key == 'latitude':
                place.latitude = post_data[key]
            if key == 'longitude':
                place.longitude = post_data[key]
            place.save()
            return place.to_hash()
    except:
        return {"code":404, "msg":"not found"}

@app.route('/states/<int:state_id>/cities/<int:city_id>/places', methods=['GET'])
def places_by_city(state_id, city_id):
    city_query = City.get(City.id == city_id, City.state == state_id)
    places = []
    query = Place.select().where(Place.city == city_query.id)
    for place in query:
        places.append(place.to_hash())
    return jsonify(places)

@app.route('/states/<int:state_id>/cities/<int:city_id>/places', methods=['POST'])
@as_json
def create_place_by_city(state_id, city_id):
    city = City.get(City.id == city_id, City.state == state_id)
    before_request()
    post_data = request.values

    new_place = Place.create(
        owner=post_data['owner'],
        name=post_data['name'],
        city=post_data['city'],
        description=post_data['description'],
        latitude=post_data['latitude'],
        longitude=post_data['longitude']
    )
    if 'number_rooms' in post_data:
        new_place.number_rooms=post_data['number_rooms']
    if 'number_bathrooms' in post_data:
        new_place.number_bathrooms=post_data['number_bathrooms']
    if 'max_guest' in post_data:
        new_place.max_guest=post_data['max_guest']
    if 'price_by_night' in post_data:
        new_place.price_by_night=post_data['price_by_night']
    new_place.save()
    return new_place.to_hash()
