from flask import request
from app import app
from app.models.base import db
from app.models.state import State
from flask_json import as_json
from app.views.return_styles import ListStyle

'''listing endpoint'''
@app.route('/states', methods=['GET'])
@as_json
def get_all_states():
    # states = []
    query = State.select()
    # for state in query:
    #     states.append(state.to_dict())
    # return jsonify(states)
    return ListStyle.list(query,request)

@app.route('/states', methods=['POST'])
@as_json
def create_new_state():
    post_data = request.values
    if 'name' not in post_data:
        return {'code':400, 'msg':'bad request'}, 400

    state_row, created = State.create_or_get(name = post_data['name'])
    if not created:
        out = {'code': 10001, 'msg': 'State already exists'}
        return out, 409
    return state_row.to_dict()

@app.route('/states/<int:number>', methods=['GET'])
@as_json
def get_single_state(number):
    try:
        query = State.get(State.id == number)
    except State.DoesNotExist:
        return {'code':404, 'msg':'state not found'}, 404
    return query.to_dict()

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
