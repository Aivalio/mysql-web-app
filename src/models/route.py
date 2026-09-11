"""Route model."""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db


class Route(db.Model):
    """A flight route (airline + source airport + destination airport)."""

    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    airlines_id: Mapped[int] = mapped_column(ForeignKey("airlines.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("airports.id"))
    destination_id: Mapped[int] = mapped_column(ForeignKey("airports.id"))

    # Relationships
    airline: Mapped["Airline"] = relationship(back_populates="routes")
    source: Mapped["Airport"] = relationship(foreign_keys=[source_id])
    destination: Mapped["Airport"] = relationship(foreign_keys=[destination_id])
    flights: Mapped[list["Flight"]] = relationship(back_populates="route")

    def __repr__(self) -> str:
        return f"<Route {self.id} airline={self.airlines_id}>"