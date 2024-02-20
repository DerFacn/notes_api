from flask import request, jsonify
from app.utils import get_user, admin_required
from app.models import User
from app.db import session
from uuid import uuid4
from app.api.auth.utils import generate_hash


@get_user
@admin_required
def get_all_users(user):
    users = session.query(User).all()
    response = [{
        "uuid": user.uuid,
        "username": user.username,
        "password_hash": user.password,
        "is_admin": user.is_admin,
        "created_at": user.created_at
    } for user in users]
    return jsonify(response), 200


@get_user
@admin_required
def get_one_user(user, user_uuid):
    user = session.query(User).filter_by(uuid=user_uuid).first()
    if not user:
        return jsonify(message=f'User with uuid "{user_uuid} not founded!"'), 404
    return jsonify({
        "uuid": user.uuid,
        "username": user.username,
        "password_hash": user.password,
        "created_at": user.created_at
    }), 200


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
    return jsonify(
        message='User created!',
        user={
            "uuid": new_user.uuid,
            "username": new_user.username,
            "password": new_user.password,
            "is_admin": new_user.is_admin,
            "created_at": new_user.created_at
        }
    ), 201


@get_user
@admin_required
def edit_user(user, user_uuid):
    user = session.query(User).filter_by(uuid=user_uuid).first()
    if not user:
        return jsonify(message='User not found!'), 404

    data = request.get_json(silent=True)

    is_admin = data.get('is_admin', None)

    user.is_admin = is_admin
    session.commit()
    return jsonify(
        message='User edited!',
        user={
            "uuid": user.uuid,
            "username": user.username,
            "password": user.password,
            "is_admin": user.is_admin,
            "created_at": user.created_at
        }
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
