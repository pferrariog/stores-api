from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from stores.extensions.database import StoreModel
from stores.extensions.database import db
from stores.extensions.schemas import StoreSchema
from stores.extensions.schemas import StoreUpdateSchema


blp = Blueprint("stores", __name__, description="Store operations")


@blp.route("/stores/<int:store_id>")
class Stores(MethodView):
    """Specific store operations"""

    @blp.response(200, StoreSchema)
    def get(self, id):
        """Get store by ID"""
        store = StoreModel.query.get_or_404(id, description="Store id not found")
        return store

    @jwt_required()
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, id):
        """Update store data"""
        raise NotImplementedError

    @jwt_required()
    @blp.response(204)
    def delete(self, id):
        """Delete store by ID"""
        store = StoreModel.query.get_or_404(id, description="Store id not found")
        db.session.delete(store)
        db.session.commit()


@blp.route("/stores")
class StoresList(MethodView):
    """Operations to all stores"""

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Get all stores from database"""
        stores = StoreModel.query.all()
        return stores

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data):
        """Insert a store in database"""
        store = StoreModel(**data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store with given name already exists")
        except SQLAlchemyError as error:
            abort(500, message=f"Error {error} while inserting store to database")
        return store
