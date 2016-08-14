from flask import request
from app import app
from app.models.base import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from flask_json import as_json
from app.views.return_styles import ListStyle

'''listing endpoint'''
@app.route('/amenities', methods=['GET'])
@as_json
def get_amenities():
    # amenities = []
    query = Amenity.select()
    # for amenity in query:
    #     amenities.append(amenity.to_dict())
    # return jsonify(amenities)
    return ListStyle.list(query,request)


@app.route('/amenities', methods=['POST'])
@as_json
def create_amenity():
    post_data = request.values
    if 'name' not in post_data:
        return {"code":404, "msg": "not found"}, 404
    
    new_amenity, created = Amenity.get_or_create(name = post_data['name'])
    if not created:
        out = {'code': 10003, 'msg': 'Name already exists'}
        return out, 409
    return new_amenity.to_dict()
        

@app.route('/amenities/<int:amenity_id>', methods=['DELETE'])
@as_json
def del_amenity(amenity_id):
    try:
        query = Amenity.get(Amenity.id == amenity_id)
    except Amenity.DoesNotExist:
        return {"code":404, "msg": "not found"}, 404
    out_dict = query.to_dict()
    query.delete_instance()
    return out_dict

@app.route('/amenities/<int:amenity_id>', methods=['GET'])
@as_json
def get_amenity_by_id(amenity_id):
    try:
        get_amenity = Amenity.get(Amenity.id == amenity_id)
    except Amenity.DoesNotExist:
        return {"code":404, "msg": "not found"}, 404
    return get_amenity.to_dict()

'''listing endpoint'''
@app.route('/places/<int:place_id>/amenities', methods=['GET'])
@as_json
def get_amenities_by_place(place_id):
    # amenities = []
    query = Amenity.select().join(PlaceAmenities).where(PlaceAmenities.place == place_id)
    # for row in query:
    #     amenities.append(row.to_dict())
    # return jsonify(amenities)
    return ListStyle.list(query,request)

@app.route('/places/<int:place_id>/amenities/<int:amenity_id>', methods=['POST'])
@as_json
def create_amenityPlace(place_id, amenity_id):
    new_place_amenity, created = PlaceAmenities.create_or_get(place=place_id, amenity=amenity_id)
    if not created:
        return {'code': 400, 'msg': 'Bad request'}, 400
    return new_place_amenity.amenity.to_dict()

@app.route('/places/<int:place_id>/amenities/<int:amenity_id>', methods=['DELETE'])
@as_json
def delete_amenityPlace(place_id, amenity_id):
    try:
        new_place_amenity = PlaceAmenities.get(PlaceAmenities.place == place_id, PlaceAmenities.amenity == amenity_id)
    except PlaceAmenities.DoesNotExist:
        return {"code":404, "msg": "not found"}, 404
    out_dict = new_place_amenity.amenity.to_dict()
    new_place_amenity.delete_instance()
    return out_dict