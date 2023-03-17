from flask import Blueprint
from src.cli import my_input
from src.models.User import User
from src.extension import db
from src.extension import bcrypt


db_commands = Blueprint("db-cli", __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Creating tables...")


@db_commands.cli.command('admin')
def admin_db():
    username = my_input("Username:")
    email = my_input("Email:")
    first_name = my_input("First Name:")
    last_name = my_input("Last Name:")
    password = my_input("Password:")
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    phone_number = my_input("Phone Number:")
    new_admin = User(username=username,
                     email=email,
                     firstname=first_name,
                     lastname=last_name,
                     password=password,
                     phone_number=phone_number,
                     is_admin=True,
                     is_seller=False,
                     )

    db.session.add(new_admin)
    db.session.commit()


@db_commands.cli.command("drop")
def drop():
    print("Dropping all tables...")
    db.drop_all()
