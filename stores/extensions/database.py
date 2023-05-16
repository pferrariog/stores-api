from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


class StoreModel(db.Model, SerializerMixin):
    """Default Store Model"""

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    products = db.relationship(
        "ProductModel", back_populates="store", cascade="all, delete"  # delete product
    )  # attribute one to many (array)
    tags = db.relationship("TagModel", back_populates="store")  # one to many (array)


class ProductModel(db.Model, SerializerMixin):
    """Default Product Model"""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="products")  # many to one
    tags = db.relationship(
        "TagModel", back_populates="products", secondary="products_tags"
    )  # many to many


class TagModel(db.Model, SerializerMixin):
    """Default Tags Model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="tags")  # many to one
    products = db.relationship(
        "ProductModel", back_populates="tags", secondary="products_tags"
    )  # many to many


class ProductsTagsModel(db.Model, SerializerMixin):
    """Secondary table to Item and Tags Relationship"""

    __tablename__ = "products_tags"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)


class UserModel(db.Model, SerializerMixin):
    """Default User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)


def init_app(app):
    """Link the database to current app"""
    db.init_app(app)
    app.db = db
    Migrate(app, db)
