"""SQLAlchemy models package."""
from src.models.airline import Airline
from src.models.airplane import Airplane
from src.models.airport import Airport
from src.models.flight import Flight
from src.models.passenger import Passenger
from src.models.route import Route

__all__ = [
    "Airline",
    "Airplane",
    "Airport",
    "Flight",
    "Passenger",
    "Route",
]