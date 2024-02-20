from flask import Blueprint
from .routes import signup, login, logout

bp = Blueprint('auth', __name__, url_prefix='/auth')

bp.add_url_rule('/signup', 'signup', signup, methods=['POST'])
bp.add_url_rule('/login', 'login', login, methods=['POST'])
bp.add_url_rule('/logout', 'logout', logout, methods=['DELETE'])
