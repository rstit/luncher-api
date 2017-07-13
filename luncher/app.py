"""The app module, containing the app factory function."""
from flask import Flask

from luncher.config import Config
from luncher.extensions import db
from luncher.auth.routes import register_routes as register_auth_routes
from luncher.meals.routes import register_routes as register_meals_routes


def create_app(config_object=Config):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_routes(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_routes(app):
    register_auth_routes(app)
    register_meals_routes(app)
