from importlib import import_module

from dynaconf import FlaskDynaconf


def init_app(app):
    """Initialize the app settings"""
    FlaskDynaconf(app)


def load_extensions(app):
    """Get all extensions from settings file"""
    for extension in app.config.get("EXTENSIONS"):
        module = import_module(extension)
        module.init_app(app)
