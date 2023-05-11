from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError
from stores.extensions.database import ProductModel
from stores.extensions.database import StoreModel
from stores.extensions.database import TagModel
from stores.extensions.database import db
from stores.extensions.schemas import TagSchema


blp = Blueprint("tag", __name__, description="Department tag operations")


@blp.route("/tag/<int:tag_id>")
class Tags(MethodView):
    """Tags operations"""

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """Get tag by ID"""
        tag = TagModel.query.get_or_404(tag_id, description="Tag id not found")
        return tag

    # @blp.arguments(TagUpdateSchema)
    @blp.response(200, TagSchema)
    def put(self):
        """Update tag by ID"""
        raise NotImplementedError

    @jwt_required()
    @blp.response(204, description="Deletes the tag if not linked to a product")
    @blp.alt_response(400, description="Abort if the tag is associated to a product")
    def delete(self, tag_id):
        """Delete tag by ID"""
        tag = TagModel.query.get_or_404(tag_id, description="Tag id not found")

        if not tag.products:
            db.session.delete(tag)
            db.session.commit()
        else:
            abort(400, message="The given tag is associated to a product and could not be deleted")


@blp.route("/stores/<string:store_id>/tag")
class StoreTags(MethodView):
    """Tags operations based on stores"""

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Get all department tags from the given store"""
        store = StoreModel.query.get_or_404(store_id, description="Store id not found")
        return store.tags

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, data, store_id):
        """Create a tag in a store"""
        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == data["name"]
        ).first():
            abort(400, message="Tag name already exists in that store")

        tag = TagModel(**data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(500, message=f"Error {error} while inserting tag to Store {id}")
        return tag


@blp.route("/products/<int:product_id>/tag/<int:tag_id>")
class ProductTags(MethodView):
    """Products and tags link operations"""

    @jwt_required()
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, product_id, tag_id):
        """Link a department tag to a product"""
        product = ProductModel.query.get_or_404(product_id, description="Product id not found")
        tag = TagModel.query.get_or_404(tag_id, description="Tag id not found")

        product.tags.append(tag)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(
                500, message=f"Error {error} while linking Tag {tag_id} and Product {product_id}"
            )

        return tag

    @jwt_required()
    @blp.response(200)
    def delete(self, product_id, tag_id):
        """Unlink a tag from a product"""
        product = ProductModel.query.get_or_404(product_id, description="Product id not found")
        tag = TagModel.query.get_or_404(tag_id, description="Tag id not found")

        product.tags.remove(tag)

        try:
            db.session.add(product)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(
                500, message=f"Error {error} while linking Tag {tag_id} and Product {product_id}"
            )

        return jsonify(message="Tag and product were unlinked", product=product, tag=tag)
