from flask import request, jsonify
from app import app
from app.models.base import db
from app.models.state import State
from flask_json import as_json

app.config['JSON_ADD_STATUS'] = False

@app.route('/states', methods=['GET'])
def get_states():
    if request.method == 'GET':
        states = []
        query = State.select()
        for state in query:
            states.append(state.to_hash())
        return jsonify(states)

@app.route('/states', methods=['POST'])
@as_json
def create_new_state():
    post_data = request.values
    state_query = State.select().where(State.name == post_data['name'])
    if state_query.exists():
        out = {'code': 1001, 'msg': 'State already exists'}
        return out, 409
    if 'name' in post_data:
        state_row = State.create(name=post_data['name'])
        return state_row.to_hash()
    else:
        return {'code':404, 'msg':'not found'}, 404

@app.route('/states/<int:number>', methods=['GET', 'DELETE'])
@as_json
def state(number):
    if request.method == 'GET':
        query = State.get(State.id == number)
        return query.to_hash()
    else:
        query = State.select().where(State.id == number).get()
        out_json = query.to_hash()
        query.delete_instance()
        return out_json
