"""Flight model."""
import datetime

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db
from src.models.associations import flights_has_passengers


class Flight(db.Model):
    """A specific flight instance (route + airplane + date)."""

    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    routes_id: Mapped[int] = mapped_column(ForeignKey("routes.id"))
    date: Mapped[datetime.date] = mapped_column(Date)
    airplanes_id: Mapped[int] = mapped_column(ForeignKey("airplanes.id"))

    # Relationships
    route: Mapped["Route"] = relationship(back_populates="flights")
    airplane: Mapped["Airplane"] = relationship(back_populates="flights")
    passengers: Mapped[list["Passenger"]] = relationship(
        secondary=flights_has_passengers,
        back_populates="flights",
    )

    def __repr__(self) -> str:
        return f"<Flight {self.id} on {self.date}>"