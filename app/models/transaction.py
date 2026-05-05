from sqlalchemy import ForeignKey, String, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True, nullable=False)

    posted_date: Mapped[str] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)

    # inflow positive, outflow negative
    amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)

    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    memo: Mapped[str | None] = mapped_column(String(256), nullable=True)