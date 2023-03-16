from src.models.BaseModel import BaseModel
from src.extension import db


# Product Model class
class Product(BaseModel):

    __tablename__ = 'products'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id', ondelete='SET NULL'), nullable=True)
    brand_id = db.Column(db.Integer, db.ForeignKey(
        'brands.id', ondelete='SET NULL'), nullable=True)
    price = db.Column(db.DECIMAL(12, 2), nullable=False)
    discount_price = db.Column(db.DECIMAL(12, 2), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=False, default=0)
    seller = db.relationship(
        'User', backref=db.backref('products', cascade='all, delete-orphan'), lazy='joined', foreign_keys=[seller_id])
