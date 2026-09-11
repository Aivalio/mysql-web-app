"""Passenger tier update service."""
from sqlalchemy import distinct, func

from src.extensions import db
from src.models import Airline, Flight, Passenger, Route


def _get_tier_for_count(flight_count: int) -> str:
    """Map flight count to a loyalty tier."""
    if flight_count <= 1:
        return "Basic"
    if flight_count <= 4:
        return "Silver"
    if flight_count == 5:
        return "Gold"
    return "Platinum"


def _get_passenger_flight_counts(airline_name: str) -> list[dict]:
    """Return flight counts per passenger for an airline."""
    rows = (
        db.session.query(
            Passenger.id.label("passenger_id"),
            Passenger.name,
            Passenger.surname,
            func.count(distinct(Flight.id)).label("total_flights"),
        )
        .select_from(Passenger)
        .join(Passenger.flights)
        .join(Flight.route)
        .join(Route.airline)
        .filter(Airline.name == airline_name)
        .group_by(Passenger.id, Passenger.name, Passenger.surname)
        .all()
    )

    return [
        {
            "passenger_id": r.passenger_id,
            "name": r.name,
            "surname": r.surname,
            "total_flights": r.total_flights,
        }
        for r in rows
    ]


def update_passenger_tiers(airline_name: str) -> int:
    """Recalculate and update tier for every passenger of an airline.

    Args:
        airline_name: The airline's name.

    Returns:
        Number of passengers updated.

    Raises:
        ValueError: If the airline has no passengers.
    """
    counts = _get_passenger_flight_counts(airline_name)
    if not counts:
        raise ValueError(f"No passengers found for airline '{airline_name}'.")

    try:
        for row in counts:
            passenger = db.session.get(Passenger, row["passenger_id"])
            passenger.tier = _get_tier_for_count(row["total_flights"])
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return len(counts)


def get_passengers_by_tier(airline_name: str, tier: str) -> list[dict]:
    """Return distinct passengers of an airline in a given tier."""
    rows = (
        db.session.query(
            Passenger.name,
            Passenger.surname,
            Passenger.tier,
        )
        .select_from(Passenger)
        .join(Passenger.flights)
        .join(Flight.route)
        .join(Route.airline)
        .filter(
            Airline.name == airline_name,
            Passenger.tier == tier,
        )
        .distinct()
        .all()
    )

    return [
        {"name": r.name, "surname": r.surname, "tier": r.tier}
        for r in rows
    ]