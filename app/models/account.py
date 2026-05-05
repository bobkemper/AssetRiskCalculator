from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    institution: Mapped[str | None] = mapped_column(String(120), nullable=True)

    # checking, savings, cd, brokerage, ira
    account_type: Mapped[str] = mapped_column(String(30), nullable=False)

    # taxable, traditional_ira, roth_ira (nullable for non-investment)
    tax_treatment: Mapped[str | None] = mapped_column(String(30), nullable=True)

    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="USD")