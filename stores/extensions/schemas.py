from marshmallow import Schema
from marshmallow import fields


class PlainProductSchema(Schema):
    """Default product schema"""

    id = fields.Int(dump_only=True)  # never receive the id by request
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    """Default store schema"""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    """Default Department Schema"""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ProductSchema(PlainProductSchema):
    """Product schema with dependencies"""

    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    """Store schema with dependencies"""

    products = fields.List(fields.Nested(PlainProductSchema(), dump_only=True))
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class TagSchema(PlainTagSchema):
    """Department schema with dependencies"""

    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class ProductUpdateSchema(Schema):
    """Product schema used to update objects"""

    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class StoreUpdateSchema(Schema):
    """Store schema used to update objects"""

    name = fields.Str()
