from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


class StoresModel(db.Model, SerializerMixin):
    """Default Store Model"""

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    products = db.relationship(
        "ProductsModel", back_populates="store", cascade="all, delete"  # delete products
    )  # attribute one to many (array)


class ProductsModel(db.Model, SerializerMixin):
    """Default Product Model"""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoresModel", back_populates="products")  # attribute many to one


def init_app(app):
    """Link the database to current app"""
    db.init_app(app)
    app.db = db
    with app.app_context():
        db.create_all()
