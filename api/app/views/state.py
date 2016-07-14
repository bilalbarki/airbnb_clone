from datetime import datetime
from flask import Flask, request, jsonify
from app import app
from app.models.base import db
from app.models.state import State
from flask_json import FlaskJSON, as_json
from index import before_request, after_request
from playhouse.shortcuts import model_to_dict
import json

app.config['JSON_ADD_STATUS'] = False

@app.route('/states', methods=['GET', 'POST'])
def states():
    if request.method == 'GET':
        before_request()
        arr = []
        query = State.select()
        for i in query:
            arr.append({"id":i.id,"created_at":i.created_at,"updated_at":i.updated_at,"name":i.name})
        after_request()
        return jsonify(arr)
    else:
        before_request()
        stateName = request.form.get('name', type=str)
        state_query = State.select().where(State.name == stateName)
        if state_query.exists():
            out = {'code': 1001, 'msg': 'State already exists'}
            after_request()
            return jsonify(out), 409
        user_row = State.create(name=stateName)
        out_json = user_row.to_hash()
        after_request()
        return jsonify(out_json)

@app.route('/states/<int:number>', methods=['GET', 'DELETE'])
def state(number):
    if request.method == 'GET':
        before_request()
        query = State.select().where(State.id == number)
        for i in query:
            arr = {"id":i.id,"created_at":i.created_at,"updated_at":i.updated_at,"name":i.name}
        after_request()
        return jsonify(arr)
    else:
        before_request()
        query = State.select().where(State.id == number).get()
        out_json = query.to_hash()
        query.delete_instance()
        after_request()
        return jsonify(out_json)
