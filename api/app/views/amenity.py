from datetime import datetime
from flask import Flask, request, jsonify
from app import app
from app.models.base import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from flask_json import FlaskJSON, as_json
from index import before_request, after_request
from playhouse.shortcuts import model_to_dict
import json

app.config['JSON_ADD_STATUS'] = False

@app.route('/amenities', methods=['GET', 'POST'])
def gamenties():
    if request.method == 'GET':
        before_request()
        arr = []
        query = Amenity.select()
        for i in query:
            arr.append(query.to_hash())
        after_request()
        return jsonify(arr)
    elif request.method == 'POST':
        before_request()
        amenityName = request.form.get('name', type=str)
        
        email_query = Amenity.select().where(Amenity.name == amenityName)
        if email_query.exists():
            out = {'code': 1003, 'msg': 'Amenity already exists'}
            after_request()
            return jsonify(out), 409
        create = Amenity.create(name = amenityName)
        
        out_json = create.to_hash()
        after_request()
        return jsonify(out_json)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delamenity(amenity_id):
    before_request()
    query = Amenity.select().where(Amenity.id == amenity_id).get()
    out_json = query.to_hash()
    query.delete_instance()
    after_request()
    return jsonify(out_json)
    
@app.route('/places/<place_id>/amenities', methods=['GET'])
def place_gamenities(place_id):
    arr = []
    query = PlaceAmenities.select().where(PlaceAmenities.place == place_id)
    for row in query:
        arr = Amenity.get(Amenity.id == row.amenity)
        amenities.append(amenity.to_hash)
    return jsonify(arr)
