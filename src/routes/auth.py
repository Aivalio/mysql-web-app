"""Authentication routes: login, logout."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from src.services.auth_service import authenticate


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Render login form and handle submission."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please fill in all fields.", "warning")
            return render_template("auth/login.html")

        user = authenticate(username, password)
        if user is None:
            flash("Invalid credentials.", "error")
            return render_template("auth/login.html")

        login_user(user)
        flash(f"Welcome, {user.username}!", "success")
        return redirect(url_for("main.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log the admin out."""
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("main.index"))