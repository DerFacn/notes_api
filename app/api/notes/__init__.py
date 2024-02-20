from flask import Blueprint
from .routes import get_one, get_all, create, update, delete

bp = Blueprint('notes', __name__, url_prefix='/notes')

bp.add_url_rule('/get', 'get_all', get_all, methods=['GET'])
bp.add_url_rule('/get/<int:note_id>', 'get_one', get_one, methods=['GET'])
bp.add_url_rule('/create', 'create', create, methods=['POST'])
bp.add_url_rule('/update/<int:note_id>', 'update', update, methods=['PUT'])
bp.add_url_rule('/delete/<int:note_id>', 'delete', delete, methods=['DELETE'])
