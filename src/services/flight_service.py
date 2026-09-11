"""Flight-related business queries."""
import datetime

from sqlalchemy import distinct, func, or_

from src.extensions import db
from src.models import Airline, Airplane, Airport, Flight, Passenger, Route


def find_alternative_flights(
    from_city: str,
    to_city: str,
    flight_date: datetime.date,
) -> list[dict]:
    """Find flights between two cities on a given date (active airlines only).

    Returns:
        List of dicts with flight_id, airline_alias,
        destination_airport, airplane_model.
    """
    source = db.aliased(Airport)
    destination = db.aliased(Airport)

    rows = (
        db.session.query(
            Flight.id.label("flight_id"),
            Airline.alias.label("airline_alias"),
            destination.name.label("destination_airport"),
            Airplane.model.label("airplane_model"),
        )
        .select_from(Flight)
        .join(Flight.route)
        .join(Route.airline)
        .join(Route.source.of_type(source))
        .join(Route.destination.of_type(destination))
        .join(Flight.airplane)
        .filter(
            Airline.active == "Y",
            source.city == from_city,
            destination.city == to_city,
            Flight.date == flight_date,
        )
        .distinct()
        .all()
    )

    return [
        {
            "flight_id": r.flight_id,
            "airline_alias": r.airline_alias,
            "destination_airport": r.destination_airport,
            "airplane_model": r.airplane_model,
        }
        for r in rows
    ]


def find_airport_visitors(
    airline_name: str,
    date_from: datetime.date,
    date_to: datetime.date,
) -> list[dict]:
    """Count distinct passengers per airport for an airline in a date range.

    Returns:
        List of dicts with airport_name and visitor_count.
    """
    rows = (
        db.session.query(
            Airport.name.label("airport_name"),
            func.count(distinct(Passenger.id)).label("visitor_count"),
        )
        .select_from(Airline)
        .join(Airline.routes)
        .join(Route.flights)
        .join(Flight.passengers)
        .join(
            Airport,
            or_(
                Route.source_id == Airport.id,
                Route.destination_id == Airport.id,
            ),
        )
        .filter(
            Airline.name == airline_name,
            Flight.date >= date_from,
            Flight.date <= date_to,
        )
        .group_by(Airport.id, Airport.name)
        .all()
    )

    return [
        {
            "airport_name": r.airport_name,
            "visitor_count": r.visitor_count,
        }
        for r in rows
    ]