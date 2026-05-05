from sqlalchemy import Date, Numeric, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class RegisterEntry(Base):
    __tablename__ = "register_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        index=True,
        nullable=False,
    )

    posted_date: Mapped[str] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    # semantic intent (opening, deposit, withdrawal, transfer_in, etc.)
    entry_type: Mapped[str] = mapped_column(String(32), nullable=False)

    # math columns (one or the other typically)
    debit: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    credit: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
