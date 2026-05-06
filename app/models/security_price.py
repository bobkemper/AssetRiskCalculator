import datetime as dt
from sqlalchemy import (
    Integer, Date, Numeric, BigInteger, String,
    DateTime, ForeignKey, Index, UniqueConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base

class SecurityPrice(Base):
    __tablename__ = "security_prices"

    __table_args__ = (
        # Enforce one row per security per date
        UniqueConstraint(
            "security_id", "trade_date",
            name="ux_security_prices_security_date"
        ),

        # Critical read patterns
        Index(
            "ix_security_prices_security_date",
            "security_id", "trade_date"
        ),
        Index(
            "ix_security_prices_trade_date",
            "trade_date"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    security_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("securities.id", ondelete="CASCADE"),
        nullable=False
    )

    trade_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    open_price: Mapped[float | None] = mapped_column(Numeric(18, 6))
    high_price: Mapped[float | None] = mapped_column(Numeric(18, 6))
    low_price:  Mapped[float | None] = mapped_column(Numeric(18, 6))
    close_price: Mapped[float | None] = mapped_column(Numeric(18, 6))
    adjusted_close: Mapped[float | None] = mapped_column(Numeric(18, 6))

    volume: Mapped[int | None] = mapped_column(BigInteger)

    # provenance
    source: Mapped[str] = mapped_column(String(32), nullable=False)  # yahoo | manual | alpha_vantage

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
