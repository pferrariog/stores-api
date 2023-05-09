from flask.views import MethodView
from flask_smorest import Blueprint
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from stores.extensions.database import ProductModel
from stores.extensions.database import db
from stores.extensions.schemas import ProductSchema
from stores.extensions.schemas import ProductUpdateSchema


blp = Blueprint("products", __name__, description="Products operations")


@blp.route("/products/<int:product_id>")
class Products(MethodView):
    """Specific product operations"""

    @blp.response(200, ProductSchema)
    def get(self, id):
        """Get product by ID"""
        product = ProductModel.query.get_or_404(id, description="Product id not found")
        return product

    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductSchema)
    def put(self, id, data):
        """Update product data"""
        product = ProductModel.query.get(id)
        if not product:
            product = ProductModel(id=id, **data)
        else:
            for key in data:
                product[key] = data["key"]

        db.session.add(product)
        db.session.commit()
        return product

    @blp.response(204)
    def delete(self, id):
        """Delete product by ID"""
        product = ProductModel.query.get_or_404(id, description="Product id not found")
        db.session.delete(product)
        db.session.commit()


@blp.route("/products")
class ProductsList(MethodView):
    """Operations to all products"""

    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """Get all products from database"""
        products = ProductModel.query.all()
        return products

    @blp.response(201, ProductSchema)
    def post(self, data):
        """Insert a product to database"""
        product = ProductModel(**data)
        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Product with given name already exists")
        except SQLAlchemyError as error:
            abort(500, message=f"Error {error} while inserting product to database")
        return product
