#!/usr/bin/python3
""""""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    result = {}
    storage.delete(place)
    storage.save()
    return jsonify(result), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_get = request.get_json()
    if not json_get:
        abort(400, "Not a JSON")
    if "user_id" not in json_get:
        abort(400, "Missing user_id")
    user = json_get['user_id']
    if not storage.get(User, user):
        abort(404)
    if 'name' not in json_get:
        abort(400, "Missing name")
    new_place = Place(**json_get)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        json_get = request.get_json()
    except:
        abort(400, "Not a JSON")
    if json_get and isinstance(json_get, dict):
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in json_get.items():
            if key not in ignore:
                setattr(place, key, value)
        storage.save()
    return jsonify(place.to_dict()), 200
