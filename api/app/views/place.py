from datetime import datetime
from flask import Flask, request, jsonify
from app import app
from app.models.base import db
from app.models.city import City
from app.models.state import State
from flask_json import FlaskJSON, as_json
from index import before_request, after_request
from playhouse.shortcuts import model_to_dict
import json

app.config['JSON_ADD_STATUS'] = False

@app.route('/places', methods=['GET', 'POST'])
def places(state_id):
    if request.method == 'GET':
        before_request()
        arr = []
        query = PlaceBook.select().where(PlaceBook.place == place_id)
        for i in query:
            #arr.append({"name":i.name, "created at":str(i.created_at), "id":str(i.id), "updated_at": str(i.updated_at), "state": i.state.name})
            arr.append(i.to_hash())
        after_request()
        return jsonify(arr)
    else:
        before_request()
        mname = request.form.get('name', type=str)
        mowner = request.form.get('name', type=str)
        mcity = request.form.get('city', type=str)
        mdescription = request.form.get('description', type=str)
        mnumber_rooms = request.form.get('number_rooms', type=str)
        mmax_guest = request.form.get('max_guest', type=str)
        mprice_by_night = request.form.get('price_by_night', type=str)
        mlatitude = request.form.get('latitude', type=str)
        mlongitude = request.form.get('longitude', type=str)
        #mcity_query = Place.select().where(Place.name == placeName)
        #mstate_query = State.select().where(State.id == state_id).get()
        '''if city_query.exists():
            out = {'code': 1003, 'msg': 'Place already exists'}
            after_request()
            return jsonify(out), 409'''
        new = Place.create(owner=mowner, name=mname, city=mcity, description=mdescription, number_rooms=mnumber_rooms, number_bathrooms=mnumber_bathrooms, max_guest=mmax_guest, price_by_night=mprice_by_night, latitude=mlatitude, longitude=mlongitude)
        #user_row = City.create(state=state_query, name=cityName)
        out_json = new.to_hash()
        after_request()
        return jsonify(out_json)

@app.route('/places/<place_id>', methods=['GET', 'DELETE'])
def place(place_id):
    if request.method == 'GET':
        before_request()
        new_place = Place.get(Place.id == place_id)
        mname = request.form.get('name', type=str)
        mdescription = request.form.get('description', type=str)
        mnumber_rooms = request.form.get('number_rooms', type=str)
        mmax_guest = request.form.get('max_guest', type=str)
        mprice_by_night = request.form.get('price_by_night', type=str)
        mlatitude = request.form.get('latitude', type=str)
        mlongitude = request.form.get('longitude', type=str)
        
        new_place.name = mname
        new_place.description = mdescription
        new_place.number_rooms = mnumber_rooms
        new_place.max_guest = mmax_guest
        new_place.price_by_night = mprice_by_night
        new_place.latitude = mlatitude
        new_place.longitude = mlongitude
    
        #arr = {"name":i.name, "created at":str(i.created_at), "id":str(i.id), "updated_at": str(i.updated_at), "state": i.state.name}
        arr = new_place.get_hash()
        after_request()
        return jsonify(arr)
    else:
        before_request()
        query = Place.get(Place.id == place_id)
        #query = City.select().where(City.id == number).get()
        out_json = query.to_hash()
        query.delete_instance()
        after_request()
        return jsonify(out_json)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['GET'])
def placesbycity(state_id, city_id):
    city = City.get(City.id == city_id, City.state == state_id)
    places = []
    query = Place.select().where(Place.city == city.id)
    for r in query:
        places.append(r.to_hash())
    return jsonify(places)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['POST'])
def create_place_by_city(state_id, city_id):
    city = City.get(City.id == city_id, City.state == state_id)
    before_request()
    mname = request.form.get('name', type=str)
    mowner = request.form.get('name', type=str)
    mcity = city.id
    mdescription = request.form.get('description', type=str)
    mnumber_rooms = request.form.get('number_rooms', type=str)
    mmax_guest = request.form.get('max_guest', type=str)
    mprice_by_night = request.form.get('price_by_night', type=str)
    mlatitude = request.form.get('latitude', type=str)
    mlongitude = request.form.get('longitude', type=str)
        #mcity_query = Place.select().where(Place.name == placeName)
        #mstate_query = State.select().where(State.id == state_id).get()

    new = Place.create(owner=mowner, name=mname, city=mcity, description=mdescription, number_rooms=mnumber_rooms, number_bathrooms=mnumber_bathrooms, max_guest=mmax_guest, price_by_night=mprice_by_night, latitude=mlatitude, longitude=mlongitude)
    out_json = new.to_hash()
    after_request()
    return jsonify(out_json)
