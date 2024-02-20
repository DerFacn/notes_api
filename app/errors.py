from flask import jsonify
from app import app


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(message='405 Method not allowed!'), 405


@app.errorhandler(404)
def not_found(e):
    return jsonify(message='404 Not found!'), 404
