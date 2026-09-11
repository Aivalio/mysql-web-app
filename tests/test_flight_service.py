"""Tests for flight_service."""
import datetime

from src.services.flight_service import (
    find_alternative_flights,
    find_airport_visitors,
)


def test_find_alternative_flights_excludes_inactive_airlines(sample_data):
    """Athens → Berlin on 2024-06-01: 2 flights (GhostAir is inactive)."""
    result = find_alternative_flights("Athens", "Berlin", datetime.date(2024, 6, 1))
    assert len(result) == 2
    aliases = {r["airline_alias"] for r in result}
    assert aliases == {"Aegean", "LH"}


def test_find_alternative_flights_unknown_city(sample_data):
    """Unknown city returns empty list."""
    result = find_alternative_flights("Atlantis", "Berlin", datetime.date(2024, 6, 1))
    assert result == []


def test_find_airport_visitors_counts_distinct_passengers(sample_data):
    """Aegean flights: Athens appears (as source) with 3 distinct pax."""
    result = find_airport_visitors(
        "Aegean Airlines",
        datetime.date(2024, 6, 1),
        datetime.date(2024, 6, 1),
    )
    # Athens and Berlin both appear as airports
    airports = {r["airport_name"] for r in result}
    assert "Athens Intl" in airports
    assert "Berlin Brand." in airports
    # Each should have 3 (all pax flew the Aegean flight)
    for r in result:
        assert r["visitor_count"] == 3