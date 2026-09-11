"""Airplane model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db
from src.models.associations import airlines_has_airplanes


class Airplane(db.Model):
    """Represents an aircraft."""

    __tablename__ = "airplanes"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str | None] = mapped_column(String(45))
    manufacturer: Mapped[str | None] = mapped_column(String(45))
    model: Mapped[str | None] = mapped_column(String(45))

    # Relationships
    airlines: Mapped[list["Airline"]] = relationship(
        secondary=airlines_has_airplanes,
        back_populates="airplanes",
    )
    flights: Mapped[list["Flight"]] = relationship(back_populates="airplane")

    def __repr__(self) -> str:
        return f"<Airplane {self.number} {self.model}>"