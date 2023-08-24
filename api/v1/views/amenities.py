#!/usr/bin/python3
""""""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def get_amenities():
    st_amenities = storage.all(Amenity)
    amenity_list = []
    for obj in st_amenities:
        amenity_list.append(st_amenities[obj].to_dict())
    return jsonify(st_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities_id(amenity_id):
    st_amenities = storage.get(Amenity, amenity_id)
    if st_amenities is not None:
        return jsonify(st_amenities.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def detele_amenity(amenity_id):
    st_amenities = storage.get(Amenity, amenity_id)
    if st_amenities is None:
        return abort(404)
    storage.delete(st_amenities)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['POST'])
def post_amenity():
    data = request.get_json()
    if not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    elif 'name' not in data:
        error_message2 = 'Missing name'
        return jsonify(error_message2), 400
    else:
        amenity = Amenity()
        amenity.name = data['name']
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    data = request.get_json()
    st_amenities = storage.get(Amenity, amenity_id)
    if st_amenities is None:
        return abort(404)
    elif not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    else:
        st_amenities.name = data['name']
        st_amenities.save()
        return jsonify(st_amenities.to_dict()), 200
