import uuid

from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    products = db.relationship(
        "ProductModel",
        back_populates="store",
        lazy="dynamic",
        cascade="all, delete",
    )
    categories = db.relationship(
        "CategoryModel",
        back_populates="store",
        lazy="dynamic",
    )
