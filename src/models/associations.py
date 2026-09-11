"""Association tables for many-to-many relationships."""
from sqlalchemy import Column, ForeignKey, Table

from src.extensions import db


# airlines <-> airplanes (many-to-many)
airlines_has_airplanes = Table(
    "airlines_has_airplanes",
    db.metadata,
    Column("airlines_id", ForeignKey("airlines.id"), primary_key=True),
    Column("airplanes_id", ForeignKey("airplanes.id"), primary_key=True),
)


# flights <-> passengers (many-to-many)
flights_has_passengers = Table(
    "flights_has_passengers",
    db.metadata,
    Column("flights_id", ForeignKey("flights.id"), primary_key=True),
    Column("passengers_id", ForeignKey("passengers.id"), primary_key=True),
)