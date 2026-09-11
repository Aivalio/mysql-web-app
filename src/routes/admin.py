"""Admin routes: update passenger tiers."""
from flask import Blueprint, flash, render_template, request
from flask_login import login_required

from src.services.passenger_service import (
    get_passengers_by_tier,
    update_passenger_tiers,
)


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/passengers/tiers", methods=["GET", "POST"])
@login_required
def update_tiers():
    passengers = None

    if request.method == "POST":
        airline_name = request.form.get("airline_name", "").strip()
        tier = request.form.get("tier", "").strip()

        if not airline_name:
            flash("Airline name is required.", "error")
            return render_template("admin/update_tiers.html", passengers=None)

        try:
            count = update_passenger_tiers(airline_name)
            flash(f"Updated {count} passenger(s) for '{airline_name}'.", "success")
        except ValueError as e:
            flash(str(e), "error")
            return render_template("admin/update_tiers.html", passengers=None)

        if tier:
            passengers = get_passengers_by_tier(airline_name, tier)

    return render_template("admin/update_tiers.html", passengers=passengers)