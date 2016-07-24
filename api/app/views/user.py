from flask import Flask, jsonify, request
from app import app
from app.models.user import User
from flask_json import as_json

app.config['JSON_ADD_STATUS'] = False

@app.route('/users', methods=['GET'])
def users():
    all_users = []
    query = User.select()
    for user in query:
        all_users.append(user.to_hash())
    return jsonify(all_users)

@app.route('/users', methods=['POST'])
@as_json
def create_new_user():
    post_data = request.values
    keys = ["first_name", "last_name", "email", "password"]
    for key in keys:
        if key not in post_data:
            return {"code":400, "msg":"incorrect parameters"}, 400
    email_query = User.select().where(User.email == post_data['email'])
    if email_query.exists():
        out = {
            'code': 1000, 
            'msg': 'Email already exists'
        }
        return out, 409
    try:
        user_row = User.create(
            password = "default",
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            email = post_data['email']
        )
        user_row.password = user_row.set_password(post_data['password'])
        if 'is_admin' in post_data:
            if post_data['is_admin'].lower() == "true":
                user_row.is_admin = True
            elif post_data['is_admin'].lower() == "false":
                user_row.is_admin = False
        user_row.save()
        return user_row.to_hash()
    except:
        return {"code":400, "msg":"incorrect parameters"}, 400

@app.route('/users/<int:number>', methods=['GET', 'PUT', 'DELETE'])
@as_json
def user(number):
    if request.method == 'GET':
        try:
            query = User.get(User.id == number)
            return query.to_hash()
        except:
            return {'error':'user does not exist'}
    elif request.method == 'PUT':
        post_data = request.values
        try:
            query = User.get(User.id == number)
        except:
            return {'error':'user does not exist'}
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
            query.set_password(post_data['password'])
        query.save()
        return query.to_hash()
    else:
        query = User.select().where(User.id == number)
        if query.exists():
            query = query.get()
            out_json = query.to_hash()
            query.delete_instance()
            return out_json
        else:
            return {"code":404, "msg":"not found"}, 404
