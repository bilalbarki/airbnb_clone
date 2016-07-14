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

@app.route('/states/<int:state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    if request.method == 'GET':
        before_request()
        arr = []
        query = (City.select(State, City).join(State).where(State.id == state_id))
        for i in query:
            arr.append({"name":i.name, "created at":str(i.created_at), "id":str(i.id), "updated_at": str(i.updated_at), "state": i.state.name})
        after_request()
        return jsonify(arr)
    else:
        before_request()
        cityName = request.form.get('name', type=str)
        city_query = City.select().where(City.name == cityName)
        state_query = State.select().where(State.id == state_id).get()
        if city_query.exists():
            out = {'code': 1002, 'msg': 'City already exists'}
            after_request()
            return jsonify(out), 409
        user_row = City.create(state=state_query, name=cityName)
        out_json = user_row.to_hash()
        after_request()
        return jsonify(out_json)

@app.route('/states/<int:state_id>/cities/<int:city_id>', methods=['GET', 'DELETE'])
def city(state_id, city_id):
    if request.method == 'GET':
        before_request()
        i = City.get(City.id == city_id, City.state == state_id)
        #for i in query:
        arr = {"name":i.name, "created at":str(i.created_at), "id":str(i.id), "updated_at": str(i.updated_at), "state": i.state.name}
        after_request()
        return jsonify(arr)
    else:
        before_request()
        query = City.get(City.id == city_id, City.state == state_id)
        #query = City.select().where(City.id == number).get()
        out_json = query.to_hash()
        query.delete_instance()
        after_request()
        return jsonify(out_json)
