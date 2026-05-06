import datetime as dt
from sqlalchemy import (
    Integer, Numeric, String, Date, DateTime,
    ForeignKey, Index, CheckConstraint, func
)
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"

    __table_args__ = (
        Index("ix_pt_portfolio_date", "portfolio_id", "trade_date"),
        Index("ix_pt_security_date", "security_id", "trade_date"),
        CheckConstraint(
            "transaction_type IN ('BUY','SELL','DIVIDEND','FEE','TRANSFER')",
            name="ck_pt_transaction_type",
        ),
        CheckConstraint(
            "(quantity IS NOT NULL AND price IS NOT NULL) "
            "OR transaction_type IN ('DIVIDEND','FEE','TRANSFER')",
            name="ck_pt_qty_price_required",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    portfolio_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
    )

    security_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("securities.id"),
        nullable=True,
    )

    transaction_type: Mapped[str] = mapped_column(String(16), nullable=False)

    trade_date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    # Units (positive for BUY, negative handled via type)
    quantity: Mapped[float | None] = mapped_column(Numeric(18, 6))

    # Price per unit (not market close, this is execution price)
    price: Mapped[float | None] = mapped_column(Numeric(18, 6))

    # Explicit cash impact (recommended for DIVIDEND / FEE)
    cash_amount: Mapped[float | None] = mapped_column(Numeric(18, 6))

    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")

    notes: Mapped[str | None] = mapped_column(String(255))

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
