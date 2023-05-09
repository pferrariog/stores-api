from flask.views import MethodView
from flask_smorest import Blueprint
from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError
from stores.extensions.database import StoresModel
from stores.extensions.database import TagsModel
from stores.extensions.database import db
from stores.extensions.schemas import TagSchema


blp = Blueprint("tag", __name__, description="Department tag operations")


@blp.route("/tag/<int:tag_id>")
class Tags(MethodView):
    """Tags operations"""

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """Get tag by ID"""
        tag = TagsModel.query.get_or_404(tag_id, description="Tag id not found")
        return tag

    # @blp.arguments(TagUpdateSchema)
    @blp.response(200, TagSchema)
    def put(self):
        """Update tag by ID"""
        raise NotImplementedError

    @blp.response(204)
    def delete(self, tag_id):
        """Delete tag by ID"""
        raise NotImplementedError


@blp.route("/stores/<string:store_id>/tag")
class StoreTags(MethodView):
    """Tags operations based on stores"""

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Get all department tags from the given store"""
        store = StoresModel.query.get_or_404(store_id, description="Store id not found")
        return store.tags

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, data, store_id):
        """Create a tag in a store"""
        if TagsModel.query.filter(
            TagsModel.store_id == store_id, TagsModel.name == data["name"]
        ).first():
            abort(400, message="Tag name already exists in that store")

        tag = TagsModel(**data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(500, message=f"Error {error} while inserting tag to Store {id}")
        return tag
