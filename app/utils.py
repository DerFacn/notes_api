from functools import wraps
from flask import request, jsonify
import jwt
from jwt.exceptions import ExpiredSignatureError
from app.models import User
from app.db import session
from app import app


def get_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['user'] = None

        access_token = request.cookies.get('access_token', None)

        if not access_token:
            return func(*args, **kwargs)

        try:
            payload = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except ExpiredSignatureError:
            return func(*args, **kwargs)

        user = session.query(User).filter_by(uuid=payload['uuid']).first()
        if not user:
            return func(*args, **kwargs)

        kwargs['user'] = user
        return func(*args, **kwargs)
    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['user'] = None

        access_token = request.cookies.get('access_token', None)

        if not access_token:
            return jsonify(message='You are not authorized!'), 403

        try:
            payload = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except ExpiredSignatureError:
            return jsonify(message='You are not authorized!'), 403

        user = session.query(User).filter_by(uuid=payload['uuid']).first()
        if not user:
            return jsonify(message='User deleted!'), 404

        kwargs['user'] = user
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not kwargs["user"].is_admin:
            return jsonify(message='Permission denied!'), 403

        return func(*args, **kwargs)
    return wrapper
