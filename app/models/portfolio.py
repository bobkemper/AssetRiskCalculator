import datetime as dt
from sqlalchemy import Integer, String, Text, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text)

    currency: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        default="USD",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
