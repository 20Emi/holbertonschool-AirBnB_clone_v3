#!/usr/bin/python3
""""""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def app_vi():
    """returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def app_vi1():
    """is added count() method from storage"""
    from models import storage
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
