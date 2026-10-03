"""Tests for config loading, admin login flow, and the password-hash generator."""
import importlib
import subprocess
import sys
from pathlib import Path

from werkzeug.security import check_password_hash, generate_password_hash

import src.config
from src.services.auth_service import authenticate


def test_config_reads_admin_password_hash_from_env(monkeypatch):
    """The config must load ADMIN_PASSWORD_HASH from the environment.

    Regression: the value was documented in .env.example but never read by the
    Config class, so admin login silently failed in any real deployment.
    """
    monkeypatch.setenv("ADMIN_PASSWORD_HASH", "scrypt:abc123")
    # The class attributes are evaluated at import time, so reload after setting
    # the env var to make the loader re-run.
    reloaded = importlib.reload(src.config)
    assert reloaded.Config.ADMIN_PASSWORD_HASH == "scrypt:abc123"


def test_config_admin_password_hash_defaults_empty(monkeypatch):
    """With no env var set, admin login is disabled (empty hash)."""
    monkeypatch.delenv("ADMIN_PASSWORD_HASH", raising=False)
    reloaded = importlib.reload(src.config)

    assert reloaded.TestConfig.ADMIN_PASSWORD_HASH == ""


def test_login_route_authenticates_admin_via_config(app, client):
    """End-to-end: set the hash via app config (as Config now does from env) and
    POST the login form -> redirect to index."""
    password_hash = generate_password_hash("s3cret!")
    app.config["ADMIN_PASSWORD_HASH"] = password_hash

    resp = client.post(
        "/auth/login",
        data={"username": "admin", "password": "s3cret!"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    # A successful login flashes a greeting.
    assert b"Welcome" in resp.data


def test_admin_tier_page_requires_login(app, client):
    """The tier-update admin page is protected by login."""
    resp = client.get("/admin/passengers/tiers")
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]


def test_authenticate_disabled_without_hash(app):
    """When no ADMIN_PASSWORD_HASH is configured, login is impossible."""
    app.config["ADMIN_PASSWORD_HASH"] = ""
    with app.app_context():
        assert authenticate("admin", "anything") is None


def test_password_hash_generator_prints_valid_hash(tmp_path):
    """The generator script emits a hash that werkzeug can verify."""
    result = subprocess.run(
        [sys.executable, "scripts/generate_password_hash.py", "pw"],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parent.parent),
    )
    assert result.returncode == 0
    generated = result.stdout.strip().splitlines()[-1]

    assert check_password_hash(generated, "pw")