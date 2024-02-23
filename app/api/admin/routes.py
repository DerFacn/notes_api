from flask import request, jsonify
from app.utils import get_user, admin_required
from app.models import User
from app.db import session
from uuid import uuid4
from app.api.auth.utils import generate_hash


@get_user
@admin_required
def get_all_users(user):
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    fields_query = request.args.get('fields', None)

    # Make a new user query
    users_query = session.query(User)

    # Add limit and offset if in query
    if limit:
        users_query = users_query.limit(limit)
    if offset:
        users_query = users_query.offset(offset)

    # Get all from database by formed query
    users = users_query.all()

    # Get all fields from User model
    available_fields = User.all_fields()

    # Forming a response
    response = []
    for user in users:
        user_dict = {}
        if fields_query:
            fields = fields_query.split(',')
            for field in fields:
                if field in available_fields:
                    user_dict[field] = getattr(user, field, None)
        else:
            for field in available_fields:
                user_dict[field] = getattr(user, field, None)
        response.append(user_dict)

    return jsonify(response), 200


@get_user
@admin_required
def get_one_user(user, user_uuid):
    user = session.query(User).filter_by(uuid=user_uuid).first()
    fields_query = request.args.get('fields', None)

    if not user:
        return jsonify(message=f'User with uuid "{user_uuid} not founded!"'), 404

    available_fields = User.all_fields()

    response = {}
    if fields_query:
        fields = fields_query.split(',')
        for field in fields:
            if field in available_fields:
                response[field] = getattr(user, field, None)
    else:
        for field in available_fields:
            response[field] = getattr(user, field, None)

    return jsonify(response), 200


@get_user
@admin_required
def create_user(user):
    data = request.get_json(silent=True)

    if not data:
        return jsonify(message='The request body must contain JSON!'), 409

    username = data.get('username', None)
    password = data.get('password', None)
    is_admin = data.get('is_admin', None)

    new_user = session.query(User).filter_by(username=username).first()
    if new_user:
        return jsonify(message='User already exists!'), 409

    identity = str(uuid4())
    password_hash = generate_hash(password)
    new_user = User(uuid=identity, username=username, password=password_hash, is_admin=is_admin)

    session.add(new_user)
    session.commit()

    available_fields = User.all_fields()

    user_dict = {}
    for field in available_fields:
        user_dict[field] = getattr(new_user, field, None)

    return jsonify(
        message='User created!',
        user=user_dict
    ), 201


@get_user
@admin_required
def edit_user(user, user_uuid):
    user = session.query(User).filter_by(uuid=user_uuid).first()
    if not user:
        return jsonify(message='User not found!'), 404

    data = request.get_json(silent=True)

    username = data.get('username', None)
    password = data.get('password', None)
    is_admin = data.get('is_admin', None)

    if username:
        user.username = username
    if password:
        user.password = generate_hash(password)
    if is_admin:
        user.is_admin = is_admin

    session.commit()

    user_dict = {}
    available_fields = User.all_fields()

    for field in available_fields:
        user_dict[field] = getattr(user, field, None)

    return jsonify(
        message='User edited!',
        user=user_dict
    ), 200


@get_user
@admin_required
def delete_user(user, user_uuid):
    user = session.query(User).filter_by(uuid=user_uuid).first()
    if not user:
        return jsonify(message='User not found!'), 404

    session.delete(user)
    session.commit()
    return jsonify(message='User deleted!'), 200
