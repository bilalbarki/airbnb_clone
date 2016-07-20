from flask import request, jsonify
from app import app
from app.models.base import db
from app.models.user import User
from app.models.amenity import Amenity
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
        query = Amenity.select().where(Amenity.name == post_data['name'])
        if query.exists():
            out = {'code': 1003, 'msg': 'Amenity already exists'}
            return out, 409
        new_amenity = Amenity.create(name = post_data['name'])
        return new_amenity.to_hash()
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
        amenities.append(amenity_query.to_hash)
    return jsonify(arr)
