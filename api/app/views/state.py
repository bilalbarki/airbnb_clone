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
        stateName = request.form.get('state', type=str)
        lastName = request.form.get('last_name', type=str)
        emailAddress = request.form.get('email', type=str)
        passwordRaw = request.form.get('password', type=str)
        isAdmin = request.form.get('is_admin', type=str)
        email_query = User.select().where(User.email == emailAddress)
        if email_query.exists():
            out = {'code': 1000, 'msg': 'Email already exists'}
            after_request()
            return jsonify(out), 409
        if isAdmin == "True":
            user_row = User.create(password="default", first_name=firstName, last_name=lastName, email=emailAddress, is_admin=True)
        else:
            user_row = User.create(password="default", first_name=firstName, last_name=lastName, email=emailAddress)
        user_row.password = user_row.set_password(passwordRaw)
        user_row.save()
        out_json = user_row.to_hash()
        after_request()
        return jsonify(out_json)

@app.route('/users/<int:number>', methods=['GET', 'PUT'])
def user(number):
    if request.method == 'GET':
        before_request()
        query = User.select().where(User.id == number)
        for i in query:
            arr = {"first_name":i.first_name,"email":i.email,"last_name":i.last_name,"is_admin":i.is_admin, "created at":str(i.created_at), "id":str(i.id), "updated_at": str(i.updated_at)}
        after_request()
        return jsonify(arr)
    else:
        before_request()
        firstName = request.form.get('first_name', type=str)
        lastName = request.form.get('last_name', type=str)
        emailAddress = request.form.get('email', type=str)
        passwordRaw = request.form.get('password', type=str)
        isAdmin = request.form.get('is_admin', type=str)
        email_query = User.select().where(User.email == emailAddress)
        query = User.select().where(User.id == number).get()
        if emailAddress != None:
            if email_query.exists():
                out = {'code': 1000, 'msg': 'Email already exists'}
                after_request()
                return jsonify(out), 409
            query.email = emailAddress
        if firstName != None:
            query.first_name = firstName
        if lastName != None:
            query.last_name = lastName
        if isAdmin != None:
            if isAdmin == "True":
                query.is_admin = True
            elif isAdmin == "False":
                query.is_admin = False
        if passwordRaw != None:
            query.set_password(passwordRaw)
        query.save()
        out_json = query.to_hash()
        after_request()
        return jsonify(out_json)
