"""Tests for passenger_service."""
import pytest

from src.models import Passenger
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