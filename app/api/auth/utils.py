from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime, timedelta
import jwt


# Passwords
def generate_hash(password: str) -> str:
    salt = gensalt()
    password_bytes = password.encode('utf-8')
    password_hash = hashpw(password_bytes, salt)
    return password_hash.decode('utf-8')


def check_hash(password: str, password_hash: str) -> bool:
    password_bytes = password.encode('utf-8')
    return checkpw(password_bytes, password_hash.encode('utf-8'))


# Cookie token
def create_token(identity):
    payload = {
        'uuid': identity,
        'exp': datetime.now() + timedelta(weeks=12)
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
