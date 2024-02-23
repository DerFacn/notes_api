import string

from flask.cli import with_appcontext
from app.models import User
from app.db import session
from app.api.auth.utils import generate_hash
from uuid import uuid4
import click
import random


@click.command('create-admin', help='Creating admin user')
@click.option('--username', prompt='Username')
@click.password_option()
@with_appcontext
def create_admin(username, password):
    identity = str(uuid4())
    password_hash = generate_hash(password)
    new_admin = User(uuid=identity, username=username, password=password_hash, is_admin=True)
    session.add(new_admin)
    session.commit()
    print('Admin user created!')


@click.command('user-seeder', help='User seeder')
@click.option('--amount', prompt='Amount of users (When generating more than 30, it may take several seconds)')
@with_appcontext
def user_seeder(amount):
    for _ in range(int(amount)):
        first_letter = random.choice(string.ascii_uppercase)
        rest = ''.join(random.choice(string.ascii_lowercase) for __ in range(6))
        identity = str(uuid4())
        password_hash = generate_hash(first_letter+rest)
        new_user = User(uuid=identity, username=first_letter+rest, password=password_hash)
        session.add(new_user)
    session.commit()
    print('Successfully created!')
