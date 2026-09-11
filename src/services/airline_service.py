"""Airline-related business queries."""
from datetime import datetime

from sqlalchemy import distinct, func

from src.extensions import db
from src.models import Airline, Airplane, Flight, Passenger, Route


def find_airline_by_age(min_age: int, max_age: int) -> dict | None:
    """Find the airline with the most passengers in the given age range.

    Args:
        min_age: Minimum age (exclusive).
        max_age: Maximum age (exclusive).

    Returns:
        Dict with airline_name, passenger_count, airplane_count or None.
    """
    current_year = datetime.now().year
    age = current_year - Passenger.year_of_birth

    row = (
        db.session.query(
            Airline.name.label("airline_name"),
            func.count(distinct(Passenger.id)).label("passenger_count"),
            func.count(distinct(Airplane.id)).label("airplane_count"),
        )
        .select_from(Airline)
        .join(Airline.airplanes)
        .join(Airline.routes)
        .join(Route.flights)
        .join(Flight.passengers)
        .filter(
            Airplane.id == Flight.airplanes_id,
            age > min_age,
            age < max_age,
        )
        .group_by(Airline.id, Airline.name)
        .order_by(func.count(distinct(Passenger.id)).desc())
        .first()
    )

    if row is None:
        return None

    return {
        "airline_name": row.airline_name,
        "passenger_count": row.passenger_count,
        "airplane_count": row.airplane_count,
    }


def find_largest_airlines() -> list[dict]:
    """Return all airlines with their fleet size and flight count, sorted.

    Returns:
        List of dicts with airline_name, airline_code,
        airplane_count, flight_count, sorted by flight_count desc.
    """
    rows = (
        db.session.query(
            Airline.name.label("airline_name"),
            Airline.code.label("airline_code"),
            func.count(distinct(Airplane.id)).label("airplane_count"),
            func.count(distinct(Flight.id)).label("flight_count"),
        )
        .select_from(Airline)
        .join(Airline.airplanes)
        .join(Airline.routes)
        .join(Route.flights)
        .filter(Airplane.id == Flight.airplanes_id)
        .group_by(Airline.id, Airline.name, Airline.code)
        .order_by(func.count(distinct(Flight.id)).desc())
        .all()
    )

    return [
        {
            "airline_name": r.airline_name,
            "airline_code": r.airline_code,
            "airplane_count": r.airplane_count,
            "flight_count": r.flight_count,
        }
        for r in rows
    ]