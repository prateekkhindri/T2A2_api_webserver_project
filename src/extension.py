from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_session import Session
from flask_msearch import Search


search = Search()

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
session = Session()
