from sqlalchemy import ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), index=True, nullable=False)
    security_id: Mapped[int] = mapped_column(ForeignKey("securities.id"), index=True, nullable=False)

    as_of_date: Mapped[str] = mapped_column(Date, nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    cost_basis_total: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)