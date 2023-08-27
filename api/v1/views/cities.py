#!/usr/bin/python3
""""""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET'])
def all_cities_state(state_id):

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    results = []
    for city in state.cities:
        results.append(city.to_dict())
    return jsonify(results)


@app_views.route('cities/<city_id>', methods=['GET'])
def only_cities(city_id):

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    results = city.to_dict()
    return jsonify(results)


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    result = {}
    storage.delete(city)
    storage.save()
    return jsonify(result), 200


@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    json_get = request.get_json()
    if not json_get:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400

    if 'name' not in json_get:
        error_message2 = 'Missing name'
        abort(error_message2), 400

    json_get['state_id'] == state.id
    json_get = City(**json_get)
    storage.new(json_get)
    storage.save()

    return jsonify(json_get.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_get = request.get_json()

    if not json_get:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in json_get.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
