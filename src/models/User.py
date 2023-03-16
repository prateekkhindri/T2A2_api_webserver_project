from src.extension import db
from src.models.BaseModel import BaseModel


class User(BaseModel):
    """ User Model class """

    __tablename__ = 'users'
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String(255), nullable=False)
    is_seller = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    @classmethod
    def find_by_email(cls, user_email):
        # Finds a user instance by email

        user = cls.query.filter_by(email=user_email).first()
        if user:
            return user
        return None

    def save_seller(self):
        self.is_seller = True
        self.save()
