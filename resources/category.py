from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CategoryModel, ProductModel, StoreModel
from schemas import CategoryAndProductSchema, CategorySchema

blp = Blueprint("categories", __name__, description="Operations on categories")


@blp.route("/store/<string:store_id>/category")
class CategorysInStore(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.categorys.all()

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data, store_id):
        if CategoryModel.query.filter(
            CategoryModel.store_id == store_id,
            CategoryModel.name == category_data["name"],
        ).first():
            abort(
                400, message="A category with that name already exists in that store."
            )

        category = CategoryModel(**category_data, store_id=store_id)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return category


@blp.route("/product/<string:product_id>/category/<string:category_id>")
class LinkCategoryToProduct(MethodView):
    @blp.response(200, CategorySchema)
    def post(self, product_id, category_id):
        product = ProductModel.query.get_or_404(product_id)
        category = CategoryModel.query.get_or_404(category_id)

        product.categorys.append(category)
        try:
            if product.store.id != category.store.id:
                abort(
                    400,
                    message="Make sure product and category belong to the same store before linking.",
                )

            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return category

    @blp.response(200, CategoryAndProductSchema)
    def delete(self, product_id, category_id):
        product = ProductModel.query.get_or_404(product_id)
        category = CategoryModel.query.get_or_404(category_id)

        product.categorys.remove(category)
        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return {
            "message": "Product removed from category",
            "product": product,
            "category": category,
        }


@blp.route("/category/<string:category_id>")
class category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @blp.response(
        202,
        description="Delete a category if no product is tagged with it",
        example={"message": "category deleted."},
    )
    @blp.response(404, description="category not found.")
    @blp.alt_response(
        400,
        description="Returned if category is assigned to one o more products. In this case, the category is not deleted.",
    )
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)

        if not category.products:
            db.session.delete(category)
            db.session.commit()
            return {"message": "category deleted."}
        abort(
            400,
            message="Coud not delete category. Make sure category is not associated with any products, then try again.",
        )
