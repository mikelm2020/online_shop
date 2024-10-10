import uuid

from db import db


class ProductModel(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(
        db.Uuid, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="products")
    categories = db.relationship(
        "CategoryModel",
        back_populates="categories",
        secondary="product_categories",
    )
