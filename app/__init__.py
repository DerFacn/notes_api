from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

cors = CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}}, supports_credentials=True)
swagger = Swagger(app)

from app import api

app.register_blueprint(api.bp)

from app.errors import app

