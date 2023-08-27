#!/usr/bin/python3
""""""

from api.v1.views import app_views
from flask import jsonify, request, abort
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
    st_reviews = storage.get(Review, review_id)
    if st_reviews is None:
        abort(404)
    return jsonify(st_reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def del_user(review_id):
    st_review = storage.get(Review, review_id)
    if st_review is None:
        return abort(404)
    storage.delete(st_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_reviews(place_id):
    data = request.get_json()
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    if not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    if 'user_id' not in data:
        error_message2 = 'Missing user_id'
        return jsonify(error_message2), 400
    user_id = data['user_id']
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    if 'text' not in data:
        error_message3 = 'Missing text'
        return jsonify(error_message3), 400
    else:
        data['place_id'] = place_id
        data = Review(**data)
        data.save()
        return jsonify(data.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    data = request.get_json()
    reviews = storage.get(Review, review_id)
    if review_id is None:
        abort(404)
    if not data:
        error_message = 'Not a JSON'
        return jsonify(error_message), 400
    for key in data:
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'update_at']:
            setattr(reviews, key, data[key])
    reviews.save()
    return jsonify(reviews.to_dict()), 200
