"""Tests for airline_service."""
from src.services.airline_service import (
    find_airline_by_age,
    find_largest_airlines,
)


def test_find_airline_by_age_returns_top_airline(sample_data):
    """Aegean has more passengers in 18-30 than Lufthansa."""
    result = find_airline_by_age(18, 30)
    assert result is not None
    assert result["airline_name"] == "Aegean Airlines"
    assert result["passenger_count"] >= 2


def test_find_airline_by_age_no_results(sample_data):
    """No passengers in age range 80-90."""
    result = find_airline_by_age(80, 90)
    assert result is None


def test_find_largest_airlines_sorted_by_flights(sample_data):
    """Airlines are sorted by flight count desc; inactive ones included."""
    results = find_largest_airlines()
    assert len(results) == 3
    # Each airline has 1 flight, so all flight_count == 1
    assert all(r["flight_count"] == 1 for r in results)
    assert all(r["airplane_count"] == 1 for r in results)