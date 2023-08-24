#!/usr/bin/python3
""""""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/', methods=['GET'])
def get_state():
    """"""
    state_storage = storage.all(State)
    state_list = []
    for obj in state_storage:
        state_list.append(state_storage[obj].to_dict())
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_setter_id(state_id):
    """"""
    state_storage = storage.get(State, state_id)
    if state_storage is not None:
        return jsonify(state_storage.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
    """"""
    state_storage = storage.get(State, state_id)
    if state_storage is None:
        return abort(404)
    storage.delete(state_storage)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/', methods=['POST'])
def post_state():
    """"""
    # Transforms the JSON body into a dictionary
    data = request.get_json()
    if not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    elif 'name' not in data:
        error_message2 = 'Missing name'
        return jsonify(error_message2), 400
    else:
        state = State()
        state.name = data['name']
        state.save()
        return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """"""
    data = request.get_json()
    state_storage = storage.get(State, state_id)
    if state_storage is None:
        return abort(404)
    if not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    else:
        state_storage.name = data['name']
        state_storage.save()
        return jsonify(state_storage.to_dict()), 200