"""Tests for auth_service."""
from werkzeug.security import generate_password_hash

from src.services.auth_service import AdminUser, authenticate


def test_authenticate_wrong_username(app):
    app.config["ADMIN_USERNAME"] = "admin"
    app.config["ADMIN_PASSWORD_HASH"] = generate_password_hash("secret")
    with app.app_context():
        assert authenticate("wrong", "secret") is None


def test_authenticate_wrong_password(app):
    app.config["ADMIN_USERNAME"] = "admin"
    app.config["ADMIN_PASSWORD_HASH"] = generate_password_hash("secret")
    with app.app_context():
        assert authenticate("admin", "wrong") is None


def test_authenticate_success(app):
    app.config["ADMIN_USERNAME"] = "admin"
    app.config["ADMIN_PASSWORD_HASH"] = generate_password_hash("secret")
    with app.app_context():
        user = authenticate("admin", "secret")
        assert user is not None
        assert isinstance(user, AdminUser)
        assert user.username == "admin"


def test_authenticate_no_hash_configured(app):
    app.config["ADMIN_USERNAME"] = "admin"
    app.config["ADMIN_PASSWORD_HASH"] = ""
    with app.app_context():
        assert authenticate("admin", "anything") is None