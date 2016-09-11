from flask import request
from app import app
from app.models.base import db
from app.models.city import City
from app.models.state import State
from flask_json import as_json
from app.views.return_styles import ListStyle

'''GET: Gets all cities with pagination, state_id must be provided in the URL <url/states/state_id/cities>'''
'''listing endpoint'''
@app.route('/states/<int:state_id>/cities', methods=['GET'])
@as_json
def get_cities(state_id):
    query = City.select().join(State).where(State.id == state_id)
    return ListStyle.list(query,request)

'''POST: Creates a new city in a state, state_id must be provided in the URL <url/states/state_id/cities>'''
@app.route('/states/<int:state_id>/cities', methods=['POST'])
@as_json
def create_new_city(state_id):
    post_data = request.values
    if 'name' not in post_data:
        return {'code': 40000, 'msg': "Missing parameters"}, 400
    try:
        city_row, created = City.get_or_create(state=state_id, name=post_data['name'])
        if not created:
            out = {'code': 10002, 'msg': 'City already exists in this state'}
            return out, 409
    except City.DoesNotExist:
        out = {'code': 10002, 'msg': 'state_id does not exist'}
        return out, 409
    return city_row.to_dict()

'''GET: Gets a single city data, state_id and city_id must be provided in the URL <url/states/state_id/cities/city_id>'''
@app.route('/states/<int:state_id>/cities/<int:city_id>', methods=['GET'])
@as_json
def get_single_city(state_id, city_id):
    try:
        query = City.get(City.id == city_id, City.state == state_id)
    except City.DoesNotExist:
        return {"code":404, "msg":"city not found"}, 404
    return query.to_dict()

'''DELETE: deletes a city, state_id and city_id must be provided in the URL <url/states/state_id/cities/city_id>'''
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
