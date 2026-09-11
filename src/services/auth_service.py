"""Authentication service for the admin user."""
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class AdminUser(UserMixin):
    """In-memory admin user (loaded from env vars, not DB)."""

    def __init__(self, username: str):
        self.id = username
        self.username = username

    def __repr__(self) -> str:
        return f"<AdminUser {self.username}>"


def authenticate(username: str, password: str) -> AdminUser | None:
    """Check credentials against admin env vars.

    Args:
        username: The submitted username.
        password: The submitted plain-text password.

    Returns:
        AdminUser if credentials match, otherwise None.
    """
    expected_user = current_app.config.get("ADMIN_USERNAME")
    expected_hash = current_app.config.get("ADMIN_PASSWORD_HASH")

    if not expected_hash:
        return None
    if username != expected_user:
        return None
    if not check_password_hash(expected_hash, password):
        return None

    return AdminUser(username)