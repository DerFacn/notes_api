from flask import Blueprint
from . import auth, notes, admin

bp = Blueprint('api', __name__, url_prefix='/api')

bp.register_blueprint(auth.bp)
bp.register_blueprint(notes.bp)
bp.register_blueprint(admin.bp)
