from flask import request, jsonify
from app import app
from app.models.base import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from flask_json import as_json

app.config['JSON_ADD_STATUS'] = False

@app.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = []
    query = Amenity.select()
    for amenity in query:
        amenities.append(amenity.to_hash())
    return jsonify(amenities)

@app.route('/amenities', methods=['POST'])
@as_json
def create_amenity():
    post_data = request.values
    if 'name' in post_data:
        query_amenity = Amenity.select().where(Amenity.name == post_data['name'])
        if query_amenity.exists():
            out = {'code': 10003, 'msg': 'Name already exists'}
            return out, 409
        new_amenity = Amenity.create(name = post_data['name'])
        if 'place_id' in post_data:
            query_place = Place.get(Place.id == int(post_data['place_id']))
            new_place_amenity = PlaceAmenities.create(place=query_place, amenity=new_amenity)
        return new_amenity.to_hash()
    # elif 'place_id' in post_data and 'amenity_id' in post_data:
    #     try:
    #         amenity_get = Amenity.select().where(Amenity.id == int(post_data['amenity_id'])).get()
    #     except:
    #         return {'code': 10004, 'msg': 'Amenity id does not exist'}
    #     try:
    #         query_place = Place.get(Place.id == int(post_data['place_id']))
    #     except:
    #         return {'code': 10005, 'msg': 'Place id does not exist'}
    #     try:
    #         new_place_amenity = PlaceAmenities.create(place=query_place, amenity=amenity_get)
    #     except:
    #         return {'code': 477, 'msg': 'Database connection error'}
    #     return amenity_get.to_hash()
    else:
        return {"code":404, "msg": "not found"}, 404

@app.route('/amenities/<int:amenity_id>', methods=['DELETE'])
@as_json
def del_amenity(amenity_id):
    try:
        query = Amenity.select().where(Amenity.id == amenity_id).get()
    except:
        return {"code":404, "msg": "not found"}, 404
    out_dict = query.to_hash()
    query.delete_instance()
    return out_dict

@app.route('/amenities/<int:amenity_id>', methods=['GET'])
@as_json
def get_amenity_by_id(amenity_id):
    try:
        get_amenity = Amenity.get(Amenity.id == amenity_id)
        return get_amenity.to_hash()
    except:
        return {"code":404, "msg": "not found"}, 404
    
@app.route('/places/<int:place_id>/amenities', methods=['GET'])
def get_amenities_by_place(place_id):
    amenities = []
    query = PlaceAmenities.select().where(PlaceAmenities.place == place_id)
    for row in query:
        amenity_query = Amenity.get(Amenity.id == row.amenity)
        amenities.append(amenity_query.to_hash())
    return jsonify(amenities)

@app.route('/places/<int:place_id>/amenities/<int:amenity_id>', methods=['POST'])
@as_json
def create_amenityPlace(place_id, amenity_id):
    try:
        amenity_get = Amenity.select().where(Amenity.id == amenity_id).get()
    except:
        return {'code': 10004, 'msg': 'Amenity id does not exist'}, 404
    try:
        query_place = Place.get(Place.id == place_id)
    except:
        return {'code': 10005, 'msg': 'Place id does not exist'}, 404
    try:
        new_place_amenity = PlaceAmenities.create(place=query_place, amenity=amenity_get)
    except:
        return {'code': 477, 'msg': 'Database connection error'}
    return amenity_get.to_hash()

@app.route('/places/<int:place_id>/amenities/<int:amenity_id>', methods=['DELETE'])
@as_json
def delete_amenityPlace(place_id, amenity_id):
    try:
        amenity_get = Amenity.select().where(Amenity.id == amenity_id).get()
    except:
        return {'code': 10004, 'msg': 'Amenity id does not exist'}, 404
    try:
        query_place = Place.get(Place.id == place_id)
    except:
        return {'code': 10005, 'msg': 'Place id does not exist'}, 404
    try:
        new_place_amenity = PlaceAmenities.get(PlaceAmenities.place==query_place, PlaceAmenities.amenity==amenity_get)
    except:
        return {'code': 477, 'msg': 'Database connection error'}
    out_dict = amenity_get.to_hash()
    new_place_amenity.delete_instance()
    return out_dict