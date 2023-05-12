from flask import Flask
from flask_smorest import Api
from stores.extensions.config import init_app
from stores.extensions.config import load_extensions
from stores.resources.departments import blp as Tags
from stores.resources.products import blp as Products
from stores.resources.stores import blp as Stores
from stores.resources.user import blp as Users


def create_app():
    """Initialize a flask instance"""
    app = Flask(__name__)

    init_app(app)
    load_extensions(app)

    api = Api(app)
    api.register_blueprint(Products)
    api.register_blueprint(Stores)
    api.register_blueprint(Tags)
    api.register_blueprint(Users)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000)
