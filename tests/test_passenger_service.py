"""Tests for passenger_service."""
import datetime

import pytest

from src.models import Airline, Airport, Passenger
from src.services.passenger_service import (
    _get_tier_for_count,
    get_passengers_by_tier,
    update_passenger_tiers,
)


def test_tier_mapping_boundaries():
    """Tier boundaries: 1=Basic, 4=Silver, 5=Gold, 6+=Platinum."""
    assert _get_tier_for_count(0) == "Basic"
    assert _get_tier_for_count(1) == "Basic"
    assert _get_tier_for_count(2) == "Silver"
    assert _get_tier_for_count(4) == "Silver"
    assert _get_tier_for_count(5) == "Gold"
    assert _get_tier_for_count(6) == "Platinum"
    assert _get_tier_for_count(100) == "Platinum"


def test_update_passenger_tiers(sample_data):
    """Passengers with 1 flight each become Basic."""
    count = update_passenger_tiers("Aegean Airlines")
    # Alice, Bob, Dave each flew 1 Aegean flight
    assert count == 3

    # Verify DB updated
    from src.extensions import db
    p1 = db.session.query(Passenger).filter_by(name="Alice").first()
    assert p1.tier == "Basic"


def test_update_passenger_tiers_unknown_airline_raises(sample_data):
    with pytest.raises(ValueError, match="No passengers found"):
        update_passenger_tiers("Nonexistent Air")


def test_get_passengers_by_tier(sample_data):
    update_passenger_tiers("Aegean Airlines")
    result = get_passengers_by_tier("Aegean Airlines", "Basic")
    names = {r["name"] for r in result}
    assert names == {"Alice", "Bob", "Dave"}


def test_update_passenger_tiers_derives_higher_tiers(app):
    """Regression for the N+1 refactor: a passenger with multiple flights on one
    airline must still get the correct higher tier (Silver/Gold/Platinum)."""
    from src.extensions import db
    from src.models import Airplane, Flight, Route

    # One airline, three flights of the same route, one passenger on all three.
    aa = Airline(name="MultiFly", alias="MF", country="FR", code="MF", active="Y")
    ap = Airport(name="Paris CDG", city="Paris", country="FR", code="CDG")
    ber = Airport(name="Berlin BER", city="Berlin", country="DE", code="BER")
    db.session.add_all([aa, ap, ber])
    db.session.flush()
    plane = Airplane(number="X1", manufacturer="Airbus", model="A320")
    db.session.add(plane)
    aa.airplanes.append(plane)
    db.session.flush()
    r = Route(airlines_id=aa.id, source_id=ap.id, destination_id=ber.id)
    db.session.add(r)
    db.session.flush()
    flights = [
        Flight(routes_id=r.id, date=datetime.date(2024, 6, 1), airplanes_id=plane.id),
        Flight(routes_id=r.id, date=datetime.date(2024, 6, 2), airplanes_id=plane.id),
        Flight(routes_id=r.id, date=datetime.date(2024, 6, 3), airplanes_id=plane.id),
        Flight(routes_id=r.id, date=datetime.date(2024, 6, 4), airplanes_id=plane.id),
        Flight(routes_id=r.id, date=datetime.date(2024, 6, 5), airplanes_id=plane.id),
    ]
    db.session.add_all(flights)
    db.session.flush()
    pax = Passenger(name="Tier", surname="Test", year_of_birth=1990, tier="Basic")
    db.session.add(pax)
    db.session.flush()
    for fl in flights:
        fl.passengers.append(pax)
    db.session.commit()

    count = update_passenger_tiers("MultiFly")
    assert count == 1
    db.session.refresh(pax)
    assert pax.tier == "Gold"  # exactly 5 flights -> Gold