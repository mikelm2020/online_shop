from marshmallow import Schema, fields


class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Str()


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class PlainCategorySchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()


class ProductSchema(PlainProductSchema):
    store_id = fields.Str(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    products = fields.List(fields.Nested(PlainProductSchema(), dump_only=True))
    categories = fields.List(fields.Nested(PlainCategorySchema()), dump_only=True)


class CategorySchema(PlainCategorySchema):
    store_id = fields.Str(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    products = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)


class CategoryAndProductSchema(Schema):
    message = fields.Str()
    product = fields.Nested(ProductSchema)
    category = fields.Nested(CategorySchema)


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegisterSchema(UserSchema):
    email = fields.Email(required=True)
