from src.models.BaseModel import BaseModel
from src.extension import db


# Category Model class
class Category(BaseModel):

    __tablename__ = 'categories'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship(
        'Product', cascade='all, delete-orphan', backref='category_products', lazy='joined')
