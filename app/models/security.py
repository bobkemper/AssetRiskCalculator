import datetime as dt
from sqlalchemy import String, Boolean, DateTime, Text, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class Security(Base):
    __tablename__ = "securities"

    __table_args__ = (
        UniqueConstraint("symbol", "exchange", name="ux_securities_symbol_exchange"),
        Index("ix_securities_symbol", "symbol"),
        Index("ix_securities_type", "security_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # identity
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # classification
    security_type: Mapped[str] = mapped_column(String(32), nullable=False)
    exchange: Mapped[str | None] = mapped_column(String(32), nullable=True)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    country: Mapped[str | None] = mapped_column(String(8), nullable=True)

    # provenance
    is_custom: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    price_source: Mapped[str | None] = mapped_column(String(32), nullable=True)
    external_id: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ✅ correct typing: datetime.datetime
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())