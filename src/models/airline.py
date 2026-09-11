"""Airline model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.extensions import db
from src.models.associations import airlines_has_airplanes


class Airline(db.Model):
    """Represents an airline company."""

    __tablename__ = "airlines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(45))
    alias: Mapped[str | None] = mapped_column(String(45))
    country: Mapped[str | None] = mapped_column(String(45))
    code: Mapped[str | None] = mapped_column(String(45))
    active: Mapped[str | None] = mapped_column(String(1))

    # Relationships
    routes: Mapped[list["Route"]] = relationship(back_populates="airline")
    airplanes: Mapped[list["Airplane"]] = relationship(
        secondary=airlines_has_airplanes,
        back_populates="airlines",
    )

    def __repr__(self) -> str:
        return f"<Airline {self.code} {self.name}>"