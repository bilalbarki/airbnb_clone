from flask import request
from app import app
from app.models.base import db
from app.models.state import State
from flask_json import as_json
from app.views.return_styles import ListStyle

'''GET: gets all users with pagination <url/states>'''
'''listing endpoint'''
@app.route('/states', methods=['GET'])
@as_json
def get_all_states():
    query = State.select()
    return ListStyle.list(query,request)

'''POST: creates a new state <url/states>'''
@app.route('/states', methods=['POST'])
@as_json
def create_new_state():
    post_data = request.values
    if 'name' not in post_data:
        return {'code': 40000, 'msg': "Missing parameters"}, 400

    state_row, created = State.create_or_get(name = post_data['name'])
    if not created:
        out = {'code': 10001, 'msg': 'State already exists'}
        return out, 409
    return state_row.to_dict()

'''GET: gets a single state <url/states/state_id>'''
@app.route('/states/<int:number>', methods=['GET'])
@as_json
def get_single_state(number):
    try:
        query = State.get(State.id == number)
    except State.DoesNotExist:
        return {'code':404, 'msg':'state not found'}, 404
    return query.to_dict()

'''DELETE: deletes a state <url/states/states_id>'''
@app.route('/states/<int:number>', methods=['DELETE'])
@as_json
def delete_state(number):
    try:
        query = State.get(State.id == number)
    except State.DoesNotExist:
        return {'code':404, 'msg':'state not found'}, 404
    out_json = query.to_dict()
    query.delete_instance()
    return out_json
