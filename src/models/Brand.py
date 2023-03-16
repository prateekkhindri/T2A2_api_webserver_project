from src.models.BaseModel import BaseModel
from src.extension import db


# Brand Model class
class Brand(BaseModel):

    __tablename__ = 'brands'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship(
        'Product', backref='brand_products', lazy='joined')
