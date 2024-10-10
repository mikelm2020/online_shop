from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ProductModel
from schemas import ProductSchema, ProductUpdateSchema

blp = Blueprint("products", __name__, description="Operations on products")


@blp.route("/product/<string:product_id>")
class Product(MethodView):
    @jwt_required()
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        product = ProductModel.query.get_or_404(product_id)
        return product

    @jwt_required()
    def delete(self, product_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(
                401,
                message="Admin privilige required.",
            )
        product = ProductModel.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted successfully"}

    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        product = ProductModel.query.get(product_id)
        if product:
            product.price = product_data["price"]
            product.name = product_data["name"]
        else:
            product = ProductModel(id=product_id, **product_data)

        db.session.add(product)
        db.session.commit()

        return product


@blp.route("/product")
class ProductList(MethodView):
    @jwt_required()
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        return ProductModel.query.all()

    # @jwt_required()
    @jwt_required(fresh=True)
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        product = ProductModel(**product_data)
        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(
                500,
                message="An error occurred while inserting the product.",
            )

        return product
