#!/usr/bin/python3
""" """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(excepetion):
    storage.close()


@app.errorhandler(404)
def Not_found(error):
    """Manafe error 404"""

    error = {
        "error": "Not found"
    }
    return jsonify(error), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
