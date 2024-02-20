from flask import request, jsonify, make_response
from .utils import generate_hash, check_hash, create_token
from app.models import User
from app.db import session
from uuid import uuid4
from datetime import datetime, timedelta


def signup():
    """
    Signup endpoint.
    ---
    tags:
        ["auth"]
    request:
        username: User username
        password: Hash
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'message': 'The request body must contain JSON!'}), 409

    username = data.get('username', None)
    password = data.get('password', None)

    if not username:
        return jsonify(message='Username is required!'), 409

    if not password:
        return jsonify(message='Password is required!'), 403

    user = session.query(User).filter_by(username=username).first()
    if user:
        return jsonify(message='User already exists!'), 403

    identity = str(uuid4())
    password_hash = generate_hash(password)
    new_user = User(uuid=identity, username=username, password=password_hash)
    session.add(new_user)
    session.commit()
    token = create_token(identity)
    response = make_response(jsonify(message='Successfully signed up!'), 201)
    response.set_cookie('access_token', token, path='/api/', secure=True, httponly=True,
                        expires=datetime.now() + timedelta(weeks=12))
    return response


def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'message': 'The request body must contain JSON!'}), 409

    username = data.get('username', None)
    password = data.get('password', None)

    if not username:
        return jsonify(message='Username is required!'), 403

    if not password:
        return jsonify(message='Password is required!'), 403

    user = session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify(message='User not found!'), 404

    if not check_hash(password, user.password):
        return jsonify(message='Wrong password!'), 403

    token = create_token(user.uuid)
    response = make_response(jsonify(message='Successfully logged in!'), 200)
    response.set_cookie('access_token', token, path='/api/', secure=True, httponly=True,
                        expires=datetime.now() + timedelta(weeks=12))
    return response


def logout():
    response = make_response('', 200)
    response.set_cookie('access_token', '', expires=0)
    return response
