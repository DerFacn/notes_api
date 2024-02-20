from flask import Blueprint
from .routes import get_all_users, get_one_user, create_user, edit_user, delete_user

bp = Blueprint('admin', __name__, url_prefix='/admin')

bp.add_url_rule('/get', 'get_all_users', get_all_users, methods=['GET'])
bp.add_url_rule('/get/<string:user_uuid>', 'get_one_user', get_all_users, methods=['GET'])
bp.add_url_rule('/create', 'create_user', create_user, methods=['POST'])
bp.add_url_rule('/edit/<string:user_uuid>', 'edit_user', edit_user, methods=['PUT'])
bp.add_url_rule('/delete/<string:user_uuid>', 'delete_user', delete_user, methods=['DELETE'])
