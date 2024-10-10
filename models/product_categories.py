import uuid

from db import db


class ProductCategories(db.Model):
    __tablename__ = "product_categories"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    product_id = db.Column(db.Uuid, db.ForeignKey("products.id"))
    category_id = db.Column(db.Uuid, db.ForeignKey("categories.id"))
