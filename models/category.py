import uuid

from db import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Uuid, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="categories")
    products = db.relationship(
        "ProductModel",
        back_populates="categories",
        secondary="product_categories",
    )
