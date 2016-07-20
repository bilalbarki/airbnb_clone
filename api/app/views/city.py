from flask import request, jsonify
from app import app
from app.models.base import db
from app.models.city import City
from app.models.state import State
from flask_json import as_json

app.config['JSON_ADD_STATUS'] = False

@app.route('/states/<int:state_id>/cities', methods=['GET'])
def get_cities(state_id):
    if request.method == 'GET':
        cities = []
        query = (City.select(State, City).join(State).where(State.id == state_id))
        for city in query:
            cities.append(city.to_hash())
        return jsonify(cities)

@app.route('/states/<int:state_id>/cities', methods=['POST'])
@as_json
def create_new_city(state_id):
    post_data = request.values
    if 'name' in post_data:
        city_query = City.select().where(City.name == post_data['name'])
        state_query = State.select().where(State.id == state_id).get()
        if city_query.exists():
            out = {'code': 1002, 'msg': 'City already exists in this state'}
            return out, 409
        city_row = City.create(state=state_query, name=post_data['name'])
        return city_row.to_hash()
    else:
        return {"code":404, "msg":"not found"}, 404

@app.route('/states/<int:state_id>/cities/<int:city_id>', methods=['GET', 'DELETE'])
@as_json
def city(state_id, city_id):
    if request.method == 'GET':
        query = City.get(City.id == city_id, City.state == state_id)
        return query.to_hash()
    else:
        query = City.get(City.id == city_id, City.state == state_id)
        out_dict = query.to_hash()
        query.delete_instance()
        return out_dict
