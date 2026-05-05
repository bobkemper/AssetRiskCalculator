from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class Security(Base):
    __tablename__ = "securities"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    asset_class: Mapped[str | None] = mapped_column(String(50), nullable=True)