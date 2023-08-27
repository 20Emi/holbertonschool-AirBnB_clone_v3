from api.v1.views import app_views
from flask import jsonify, request, abort
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    """
        Returns Review in a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_of_reviews = []
    for reviews in place.reviews:
        list_of_reviews.append(reviews.to_dict())
    return jsonify(list_of_reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """
        Returns the review with the specified id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
        Deletes a review obj given its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
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
def update_review(review_id):
    """
        update existing review object
    """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    for key, value in body_request.items():
        if key != 'id' and key != 'user_id' and 'place_id':
            if key != 'created_at' and key != 'updated_at':
                setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
