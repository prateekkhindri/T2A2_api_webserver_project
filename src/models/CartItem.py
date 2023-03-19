from src.models.BaseModel import BaseModel
from src.extension import db


# CartItem Model class
class CartItem(BaseModel):

    __tablename__ = 'cart_items'
    # user_id = db.Column(db.Integer, db.ForeignKey(
    #     "users.id", ondelete='CASCADE'), nullable=False)
    # seller_id = db.Column(
    #     db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey(
        'carts.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    # user = db.relationship(
    #     'User', backref='cart_items', lazy='joined', foreign_keys=[user_id])
    product = db.relationship(
        'Product', backref=db.backref('cart_items', cascade='all, delete-orphan'), lazy='joined', foreign_keys=[product_id])
