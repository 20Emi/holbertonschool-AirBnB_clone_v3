#!/usr/bin/python3
""""""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_place(place_id):
    """"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    reviews_list = []
    for review in places.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_reviews(review_id):
    """"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create new review obj """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    obj_data = request.get_json()
    if not obj_data:
        abort(400, "Not a JSON")
    if "user_id" not in obj_data:
        abort(400, "Missing user_id")
    user_id = obj_data['user_id']
    if not storage.get(User, user_id):
        abort(404)
    if "text" not in obj_data:
        abort(400, "Missing text")
    obj = Review(**obj_data)
    setattr(obj, 'place_id', place_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    data = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if data is None:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    for key in data:
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'update_at']:
            setattr(review, key, data[key])
    review.save()
    return jsonify(review.to_dict()), 200
