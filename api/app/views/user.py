from flask import request
from app import app
from app.models.user import User
from flask_json import as_json
from app.views.return_styles import ListStyle

'''receives post data for user and returns a dict'''
def user_dict(first_name = None, last_name = None, email = None, password = None, is_admin = None):
    values = {}
    if 'first_name' != None:
        values['first_name']= first_name
    if 'last_name' != None:
        values['last_name'] = last_name
    if 'email' != None:
        values['email'] = email
    if 'password' != None:
        values['password']= password
    if is_admin != None and is_admin.lower() == "true":
        values['is_admin'] = True
    return values

'''GET: Gets all users with pagination <url/users>'''
'''listing endpoint'''
@app.route('/users', methods=['GET'])
@as_json
def get_all_users():
    # all_users = []
    query = User.select()
    return ListStyle.list(query,request)
    # for user in query:
    #     all_users.append(user.to_dict())
    # return jsonify(all_users)

'''POST: creates a new user <url/users>'''
@app.route('/users', methods=['POST'])
@as_json
def create_new_user():
    post_data = request.values
    # parameters validations
    keys = ["first_name", "last_name", "email", "password"]
    for key in keys:
        if key not in post_data:
            return {'code': 40000, 'msg': "Missing parameters"}, 400

    user_dictionary = user_dict(
                post_data['first_name'], 
                post_data['last_name'], 
                post_data['email'], 
                post_data['password'],
                post_data.get('is_admin')
            )
    
    user_row, created = User.create_or_get(**user_dictionary)
    if not created:
        out = {
            'code': 10000, 
            'msg': 'Email already exists'
        }
        return out, 409
    return user_row.to_dict()

'''PUT: changes existing user info <url/users/user_id>'''
@app.route('/users/<int:number>', methods=['PUT'])
@as_json
def update_user(number):
    post_data = request.values

    try:
        query = User.get(User.id == number)
    except User.DoesNotExist:
        return {'code': 40001, 'msg':'user does not exist'}, 404
    
    if 'first_name' in post_data:
        query.first_name = post_data['first_name']
    if 'last_name' in post_data:
        query.last_name = post_data['last_name']
    if 'is_admin' in post_data:
        if post_data['is_admin'].lower() == "true":
            query.is_admin = True
        elif post_data['is_admin'].lower() == "false":
            query.is_admin = False
    if 'password' in post_data:
        query.password = query.set_password(post_data['password'])
    query.save()
    return query.to_dict()

'''DELETE: deletes a user <url/users/user_id>'''
@app.route('/users/<int:number>', methods=['DELETE'])
@as_json
def delete_user(number):
    try:
        query = User.get(User.id == number)
    except User.DoesNotExist:
        return {"code":40001, "msg":"not found"}, 404
    query = query.get()
    out_json = query.to_dict()
    query.delete_instance()
    return out_json

'''GET: gets a single user <url/users/user_id>'''
@app.route('/users/<int:number>', methods=['GET'])
@as_json
def get_user(number):
    try:
        query = User.get(User.id == number)
    except User.DoesNotExist:
        return {'code':40001, 'error':'user does not exist'}, 404
    return query.to_dict()
