"""Passenger model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db
from src.models.associations import flights_has_passengers


class Passenger(db.Model):
    """Represents a passenger."""

    __tablename__ = "passengers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(45))
    surname: Mapped[str | None] = mapped_column(String(45))
    year_of_birth: Mapped[int | None]
    tier: Mapped[str | None] = mapped_column(String(10))

    # Relationships
    flights: Mapped[list["Flight"]] = relationship(
        secondary=flights_has_passengers,
        back_populates="passengers",
    )

    def __repr__(self) -> str:
        return f"<Passenger {self.name} {self.surname}>"