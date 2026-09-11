"""Flask application factory."""
from flask import Flask

from src.config import Config
from src.extensions import db, login_manager


def create_app(config_class: type = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Admin login required."
    login_manager.login_message_category = "warning"

    # Import models so SQLAlchemy knows about them
    from src import models  # noqa: F401

    # Register blueprints
    from src.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app


@login_manager.user_loader
def load_user(user_id: str):
    """Flask-Login callback: load user by ID (from session)."""
    from src.services.auth_service import AdminUser
    return AdminUser(user_id)