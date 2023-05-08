from flask.views import MethodView
from flask_smorest import Blueprint
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from stores.extensions.database import StoresModel
from stores.extensions.database import db
from stores.extensions.schemas import StoreSchema
from stores.extensions.schemas import StoreUpdateSchema


blp = Blueprint("stores", __name__, description="Store operations")


@blp.route("/stores/<string:store_id>")
class Stores(MethodView):
    """Specific store operations"""

    @blp.response(200, StoreSchema)
    def get(self, id):
        """Get store by ID"""
        store = StoresModel.query.get_or_404(id, description="Store id not found")
        return store

    @blp.arguments(StoreUpdateSchema)
    @blp.response(201, StoreSchema)
    def put(self, id):
        """Update store data"""
        raise NotImplementedError

    @blp.response(204)
    def delete(self, id):
        """Delete store by ID"""
        store = StoresModel.query.get_or_404(id, description="Store id not found")
        db.session.delete(store)
        db.session.commit()


@blp.route("/stores")
class StoresList(MethodView):
    """Operations to all stores"""

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Get all stores from database"""
        stores = StoresModel.query.all()
        return stores

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, data):
        """Insert a store in database"""
        store = StoresModel(**data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, description="Store with given name already exists")
        except SQLAlchemyError as error:
            abort(500, description=f"Error {error} while inserting product to database")
        return store
