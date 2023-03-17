from src.extension import db
from src.models.BaseModel import BaseModel


class Address(BaseModel):
    __tablename__ = 'addresses'
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete='CASCADE'), nullable=False)
    street_address = db.Column(db.String(50), nullable=False)
    suburb = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    default = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship(
        'User', backref=db.backref('addresses', cascade='all, delete-orphan'), lazy='joined', foreign_keys=[user_id])
