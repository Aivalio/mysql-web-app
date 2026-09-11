"""Shared pytest fixtures for the Flight Search test suite."""
import datetime

import pytest

from src import create_app
from src.config import TestConfig
from src.extensions import db
from src.models import (
    Airline,
    Airplane,
    Airport,
    Flight,
    Passenger,
    Route,
)


@pytest.fixture
def app():
    """Create a Flask app with an in-memory SQLite DB."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(app):
    """Expose the SQLAlchemy session."""
    return db.session


@pytest.fixture
def client(app):
    """Flask test client (for route tests)."""
    return app.test_client()


@pytest.fixture
def sample_data(app):
    """Populate the in-memory DB with deterministic test data.

    Structure:
        - Airlines: Aegean (active), Lufthansa (active), GhostAir (inactive)
        - Airports: Athens (ATH), Berlin (BER), London (LHR)
        - Airplanes: A1, A2, A3
        - Routes: Aegean ATH→BER, Lufthansa ATH→BER, GhostAir ATH→BER
        - Flights on 2024-06-01:
            F1 (Aegean, route1, A1)
            F2 (Lufthansa, route2, A2)
            F3 (GhostAir, route3, A3)
        - Passengers:
            P1 (25yo) on F1  → Aegean
            P2 (28yo) on F1  → Aegean
            P3 (45yo) on F2  → Lufthansa
            P4 (22yo) on F1 & F2 → both
    """
    session = db.session

    # --- Airlines ---
    aegean = Airline(name="Aegean Airlines", alias="Aegean", country="Greece", code="A3", active="Y")
    lufthansa = Airline(name="Lufthansa", alias="LH", country="Germany", code="LH", active="Y")
    ghost = Airline(name="GhostAir", alias="GA", country="Nowhere", code="GA", active="N")
    session.add_all([aegean, lufthansa, ghost])
    session.flush()

    # --- Airports ---
    athens = Airport(name="Athens Intl", city="Athens", country="Greece", code="ATH")
    berlin = Airport(name="Berlin Brand.", city="Berlin", country="Germany", code="BER")
    london = Airport(name="Heathrow", city="London", country="UK", code="LHR")
    session.add_all([athens, berlin, london])
    session.flush()

    # --- Airplanes ---
    a1 = Airplane(number="A1", manufacturer="Airbus", model="A320")
    a2 = Airplane(number="A2", manufacturer="Boeing", model="737")
    a3 = Airplane(number="A3", manufacturer="Airbus", model="A321")
    session.add_all([a1, a2, a3])
    session.flush()

    # Associate airplanes with airlines (M2M)
    aegean.airplanes.append(a1)
    lufthansa.airplanes.append(a2)
    ghost.airplanes.append(a3)

    # --- Routes ---
    r1 = Route(airlines_id=aegean.id, source_id=athens.id, destination_id=berlin.id)
    r2 = Route(airlines_id=lufthansa.id, source_id=athens.id, destination_id=berlin.id)
    r3 = Route(airlines_id=ghost.id, source_id=athens.id, destination_id=berlin.id)
    session.add_all([r1, r2, r3])
    session.flush()

    # --- Flights ---
    d = datetime.date(2024, 6, 1)
    f1 = Flight(routes_id=r1.id, date=d, airplanes_id=a1.id)
    f2 = Flight(routes_id=r2.id, date=d, airplanes_id=a2.id)
    f3 = Flight(routes_id=r3.id, date=d, airplanes_id=a3.id)
    session.add_all([f1, f2, f3])
    session.flush()

    # --- Passengers ---
    p1 = Passenger(name="Alice", surname="A", year_of_birth=2001, tier="Basic")  # ~25
    p2 = Passenger(name="Bob", surname="B", year_of_birth=1998, tier="Basic")    # ~28
    p3 = Passenger(name="Carol", surname="C", year_of_birth=1981, tier="Basic")  # ~45
    p4 = Passenger(name="Dave", surname="D", year_of_birth=2004, tier="Basic")   # ~22
    session.add_all([p1, p2, p3, p4])
    session.flush()

    # --- Assign passengers to flights (M2M) ---
    f1.passengers.extend([p1, p2, p4])   # Aegean: 3 passengers (2 in 18-30: p1, p2, p4)
    f2.passengers.extend([p3, p4])       # Lufthansa: 2 passengers (p4 in range)
    f3.passengers.append(p1)             # GhostAir: 1 passenger

    session.commit()
    yield
    session.rollback()