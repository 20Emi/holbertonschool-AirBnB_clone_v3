#!/usr/bin/python3
""""""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.city import City


@app_views.route('states/<state_id>/cities', methods=['GET'])
def all_cities_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify(), 404)
    result = [city.to_dict() for city in state.cities]
    return jsonify(result)


@app_views.route('cities/<city_id>', methods=['GET'])
def only_cities(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    results= []
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
    return jsonify(result), 204

@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        json_get = request.get_json()
    except:
        abort(400, "Not a JSON")
    if 'name' not in json_get:
        abort(400, "Missing name")
    new_city = City(name=json_get['name'], state_id=state.id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city= storage.get(City, city_id)
    if not city:
        abort(404)    
    try:
        json_get = request.get_json()
    except:
        abort(400, "Not a JSON")
    if json_get and isinstance(json_get, dict):
        ignore = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in json_get.items():
            if key not in ignore:
                setattr(city, key, value)
        storage.save()
    return jsonify(city.to_dict()), 200
