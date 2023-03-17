from src.models.BaseModel import BaseModel
from src.extension import db


# Cart Model class
class Cart(BaseModel):

    __tablename__ = 'carts'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), unique=True, nullable=False)
    owner = db.relationship(
        'User', backref=db.backref('cart', cascade='all, delete-orphan'), lazy='joined', foreign_keys=[user_id])
    items = db.relationship(
        'CartItem', backref='cart', cascade='all, delete-orphan', lazy='joined')
