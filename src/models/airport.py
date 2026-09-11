"""Airport model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.extensions import db


class Airport(db.Model):
    """Represents an airport."""

    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(45))
    city: Mapped[str | None] = mapped_column(String(45))
    country: Mapped[str | None] = mapped_column(String(45))
    code: Mapped[str | None] = mapped_column(String(45))

    def __repr__(self) -> str:
        return f"<Airport {self.code} {self.city}>"