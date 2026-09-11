"""Flask application factory."""
from flask import Flask

from src.config import Config
from src.extensions import db


def create_app(config_class: type = Config) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_class: Configuration class to load (default: Config).

    Returns:
        Configured Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Import models so SQLAlchemy knows about them
    from src import models  # noqa: F401

    return app