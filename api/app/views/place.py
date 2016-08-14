from flask import request
from app import app
from app.models.city import City
from app.models.state import State
from app.models.place import Place
from app.models.place_book import PlaceBook
from flask_json import as_json
from datetime import datetime, timedelta
from app.views.return_styles import ListStyle

# def place_dict(name = None, description = None, number_rooms = None, number_bathrooms = None, max_guest = None, price_by_night = None, latitude = None, longitude = None, owner_id = None, city_id = None):
#     values = {
#         'owner': int(owner_id),
#         'name': name,
#         'city': int(city_id),
#         'description': description,
#         'latitude': float(latitude),
#         'longitude': float(longitude),
#     }
#     if number_rooms != None:
#         values['number_rooms'] = int(number_rooms)
#     if number_bathrooms != None:
#         values['number_bathrooms'] = int(number_bathrooms)
#     if max_guest != None:
#         values['max_guest'] = int(max_guest)
#     if price_by_night != None:
#         values['price_by_night'] = int(price_by_night)
#     return values

def place_dict(name = None, description = None, number_rooms = None, number_bathrooms = None, max_guest = None, price_by_night = None, latitude = None, longitude = None, owner_id = None, city_id = None):
    values = {}
    if name != None:
        values['name'] = name
    if description != None:
        values['description'] = description
    if number_rooms != None:
        values['number_rooms'] = int(number_rooms)
    if number_bathrooms != None:
        values['number_bathrooms'] = int(number_bathrooms)
    if max_guest != None:
        values['max_guest'] = int(max_guest)
    if price_by_night != None:
        values['price_by_night'] = int(price_by_night)
    if latitude != None:
        values['latitude'] = float(latitude)
    if longitude != None:
        values['longitude'] = float(longitude)
    if owner_id != None:
        values['owner'] = int(owner_id)
    if city_id != None:
        values['city'] = int(city_id)
    return values

'''listing endpoint'''
@app.route('/places', methods=['GET'])
@as_json
def get_places():
    places = []
    query = Place.select()
    # for place in query:
    #     places.append(place.to_dict())
    # return jsonify(places)
    return ListStyle.list(query,request)

@app.route('/places', methods=['POST'])
@as_json
def create_new_place():
    post_data = request.values
    keys = ['owner_id', 'name', 'city_id', 'description', 'latitude', 'longitude']
    for key in keys:
        if key not in post_data:
            return {"code":404, "msg":"Incomplete parameters"}, 404

    place_dictionary = place_dict(
        post_data['name'],
        post_data['description'],
        post_data.get('number_rooms'),
        post_data.get('number_bathrooms'),
        post_data.get('max_guest'),
        post_data.get('price_by_night'),
        post_data['latitude'],
        post_data['longitude'],
        post_data['owner_id'],
        post_data['city_id'],       
    )
    try:
        new_place = Place.create(**place_dictionary)
    except:
        return {"code":404, "msg":"Parameters not correct"}, 404
    return new_place.to_dict()

@app.route('/places/<int:place_id>', methods=['GET'])
@as_json
def get_single_place(place_id):
    try:
        new_place = Place.get(Place.id == place_id)
    except Place.DoesNotExist:
        return {'code':404, "msg":"not found"}, 404
    return new_place.to_dict()

@app.route('/places/<int:place_id>', methods=['DELETE'])
@as_json
def delete_single_place(place_id):
    try:
        query = Place.get(Place.id == place_id)
    except Place.DoesNotExist:
        return {'code':404, "msg":"place does not exist"}, 404
    out_dict = query.to_dict()
    query.delete_instance()
    return out_dict

@app.route('/places/<int:place_id>', methods=['PUT'])
@as_json
def put_place(place_id):
    post_data = request.values
    try:
        place = Place.get(Place.id == place_id)
    except Place.DoesNotExist:
        return {"code":404, "msg":"not found"}, 404
    
    # place_dictionary = place_dict(
    #     post_data.get('name'),
    #     post_data.get('description'),
    #     post_data.get('number_rooms'),
    #     post_data.get('number_bathrooms'),
    #     post_data.get('max_guest'),
    #     post_data.get('price_by_night'),
    #     post_data.get('latitude'),
    #     post_data.get('longitude'),      
    # )

    # q = Place.update(**place_dictionary).where(Place.id == place_id)
    # q.execute()
    # print q
    # if q == 1:
    #     place = Place.get(Place.id == place_id)
    #     return place.to_dict()
    # else:
    #     return {"code":404, "msg":"not found"}, 404
    # return {"code":404, "msg":"not found"}, 404
    
    if 'name' in post_data:
        place.name = post_data['name']
    if 'description' in post_data:
        place.description = post_data['description']
    if 'number_rooms' in post_data:
        place.number_rooms = int(post_data['number_rooms'])
    if 'number_bathrooms' in post_data:
        place.number_bathrooms = int(post_data['number_bathrooms'])
    if 'max_guest' in post_data:
        place.max_guest = int(post_data['max_guest'])
    if 'price_by_night' in post_data:
        place.price_by_night = int(post_data['price_by_night'])
    if 'latitude' in post_data:
        place.latitude = float(post_data['latitude'])
    if 'longitude' in post_data:
        place.longitude = float(post_data['longitude'])
    place.save()
    return place.to_dict()

'''listing endpoint'''
@app.route('/states/<int:state_id>/cities/<int:city_id>/places', methods=['GET'])
@as_json
def places_by_city(state_id, city_id):
    # places = []
    query = Place.select().join(City).where(Place.city == city_id, City.state == state_id)

    # for place in query:
    #     places.append(place.to_dict())
    # return jsonify(places)
    return ListStyle.list(query,request)

@app.route('/states/<int:state_id>/cities/<int:city_id>/places', methods=['POST'])
@as_json
def create_place_by_city(state_id, city_id):
    post_data = request.values
    keys=["name", "description", "latitude", "longitude", "owner_id"]
    for key in keys:
        if key not in post_data:
            return {"code":400, "msg":"bad request, incorrect parameters"}

    try:
        city = City.get(City.id == city_id, City.state == state_id)
    except City.DoesNotExist:
        return {"code":400, "msg":"bad request, city or state does not exist"}, 400

    place_dictionary = place_dict(
        post_data['name'],
        post_data['description'],
        post_data.get('number_rooms'),
        post_data.get('number_bathrooms'),
        post_data.get('max_guest'),
        post_data.get('price_by_night'),
        post_data['latitude'],
        post_data['longitude'],
        post_data['owner_id'],
        city.id,       
    )
    try:
        new_place = Place.create(**place_dictionary)
    except:
        return {"code":400, "msg":"Bad Request"}, 400

    return new_place.to_dict()

'''listing endpoint'''
@app.route('/states/<int:state_id>/places', methods=['GET'])
@as_json
def places_by_state(state_id):
    query = Place.select().join(City).where(City.state == state_id)
    # places = []
    # for place in query:
    #     places.append(place.to_dict())
    # return jsonify(places)
    return ListStyle.list(query,request)

@app.route('/places/<int:place_id>/available', methods=['POST'])
@as_json
def check_places_availability(place_id):
    post_data = request.values
    
    keys = ['year', 'month', 'day']
    for key in keys:
        if key not in post_data:
            return {"code":400, "msg":"Bad Request"}, 400
    
    query = PlaceBook.select().where(PlaceBook.place == place_id)
    if not query.exists():
        return {"code":400, "msg":"Bad Request, place does not exist"}, 400
    
    date_req = "%s/%s/%s" % (post_data['year'], post_data['month'], post_data['day'])
    dt = datetime.strptime(date_req, "%Y/%m/%d").date()
    
    for booking in query:
        end_date = booking.date_start.date() + timedelta(days=booking.number_nights)
        if booking.date_start.date() <= dt <= end_date:
            available = False
            break
        else:
            available = True
    
    return {
        "available": available
    }
    