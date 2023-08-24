#!/usr/bin/python3
""""""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users/', methods=['GET'])
def get_users():
    st_users = storage.all(User)
    user_list = []
    for obj in st_users:
        user_list.append(st_users[obj].to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_id(user_id):
    st_user = storage.get(User, user_id)
    if st_user is not None:
        return jsonify(st_user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def detele_user(user_id):
    st_user = storage.get(User, user_id)
    if st_user is None:
        return abort(404)
    storage.delete(st_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def post_user():
    data = request.get_json()
    if not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    elif 'email' not in data:
        error_message2 = 'Missing email'
        return jsonify(error_message2), 400
    elif 'password' not in data:
        error_message3 = 'Missing password'
        return jsonify(error_message3), 400
    else:
        users = User()
        users.email = data['email']
        users.password = data['password']
        users.save()
        return jsonify(users.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'])
def put_user(user_id):
    data = request.get_json()
    st_users = storage.get(User, user_id)
    if st_users is None:
        return abort(404)
    elif not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    st_users.email = data['email']
    st_users.save()
    return jsonify(st_users.to_dict()), 200
