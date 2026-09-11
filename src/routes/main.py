"""Main routes: home and the five query pages."""
import datetime

from flask import Blueprint, flash, render_template, request

from src.services.airline_service import (
    find_airline_by_age,
    find_largest_airlines,
)
from src.services.flight_service import (
    find_alternative_flights,
    find_airport_visitors,
)


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


# --- 1. Airline by Age ---
@main_bp.route("/airlines/by-age", methods=["GET", "POST"])
def airline_by_age():
    result = None
    if request.method == "POST":
        try:
            min_age = int(request.form.get("min_age", 0))
            max_age = int(request.form.get("max_age", 0))
        except ValueError:
            flash("Please enter valid numbers for ages.", "error")
            return render_template("airline_by_age.html", result=None)

        if min_age >= max_age:
            flash("Minimum age must be less than maximum age.", "error")
            return render_template("airline_by_age.html", result=None)

        result = find_airline_by_age(min_age, max_age)
        if result is None:
            flash("No airline found for this age range.", "warning")

    return render_template("airline_by_age.html", result=result)


# --- 2. Airport Visitors ---
@main_bp.route("/airports/visitors", methods=["GET", "POST"])
def airport_visitors():
    results = None
    airline_name = ""
    date_from = ""
    date_to = ""

    if request.method == "POST":
        airline_name = request.form.get("airline_name", "").strip()
        date_from_str = request.form.get("date_from", "")
        date_to_str = request.form.get("date_to", "")

        if not airline_name or not date_from_str or not date_to_str:
            flash("All fields are required.", "error")
            return render_template("airport_visitors.html", results=None)

        try:
            date_from = datetime.date.fromisoformat(date_from_str)
            date_to = datetime.date.fromisoformat(date_to_str)
        except ValueError:
            flash("Invalid date format.", "error")
            return render_template("airport_visitors.html", results=None)

        if date_from > date_to:
            flash("'Date from' must be before 'Date to'.", "error")
            return render_template("airport_visitors.html", results=None)

        results = find_airport_visitors(airline_name, date_from, date_to)
        if not results:
            flash(f"No visitors found for '{airline_name}' in this range.", "warning")

    return render_template(
        "airport_visitors.html",
        results=results,
        airline_name=airline_name,
        date_from=date_from,
        date_to=date_to,
    )


# --- 3. Alternative Flights ---
@main_bp.route("/flights/alternatives", methods=["GET", "POST"])
def alternative_flights():
    results = None
    from_city = ""
    to_city = ""
    flight_date = ""

    if request.method == "POST":
        from_city = request.form.get("from_city", "").strip()
        to_city = request.form.get("to_city", "").strip()
        flight_date_str = request.form.get("flight_date", "")

        if not from_city or not to_city or not flight_date_str:
            flash("All fields are required.", "error")
            return render_template("alternative_flights.html", results=None)

        try:
            flight_date = datetime.date.fromisoformat(flight_date_str)
        except ValueError:
            flash("Invalid date format.", "error")
            return render_template("alternative_flights.html", results=None)

        results = find_alternative_flights(from_city, to_city, flight_date)
        if not results:
            flash(f"No flights found from {from_city} to {to_city}.", "warning")

    return render_template(
        "alternative_flights.html",
        results=results,
        from_city=from_city,
        to_city=to_city,
        flight_date=flight_date,
    )


# --- 4. Largest Airlines ---
@main_bp.route("/airlines/largest")
def largest_airlines():
    results = find_largest_airlines()
    return render_template("largest_airlines.html", results=results)