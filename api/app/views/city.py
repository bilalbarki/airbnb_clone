from flask import request
from app import app
from app.models.base import db
from app.models.city import City
from app.models.state import State
from flask_json import as_json
from app.views.return_styles import ListStyle

'''listing endpoint'''
@app.route('/states/<int:state_id>/cities', methods=['GET'])
@as_json
def get_cities(state_id):
    # cities = []
    query = City.select().join(State).where(State.id == state_id)
    # for city in query:
    #     cities.append(city.to_dict())
    # return jsonify(cities)
    return ListStyle.list(query,request)

@app.route('/states/<int:state_id>/cities', methods=['POST'])
@as_json
def create_new_city(state_id):
    post_data = request.values
    test = request.values.get
    if 'name' not in post_data:
        return {"code":404, "msg":"not found"}, 404
    
    city_row, created = City.get_or_create(state=state_id, name=post_data['name'])
    if not created:
        out = {'code': 10002, 'msg': 'City already exists in this state'}
        return out, 409
    return city_row.to_dict()

@app.route('/states/<int:state_id>/cities/<int:city_id>', methods=['GET'])
@as_json
def get_single_city(state_id, city_id):
    try:
        query = City.get(City.id == city_id, City.state == state_id)
    except City.DoesNotExist:
        return {"code":404, "msg":"city not found"}, 404
    return query.to_dict()

@app.route('/states/<int:state_id>/cities/<int:city_id>', methods=['DELETE'])
@as_json
def delete_single_city(state_id, city_id):
    try:
        query = City.get(City.id == city_id, City.state == state_id)
    except City.DoesNotExist:
        return {"code":404, "msg":"city not found"}, 404
    out_dict = query.to_dict()
    query.delete_instance()
    return out_dict
