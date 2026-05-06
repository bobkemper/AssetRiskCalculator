from sqlalchemy import select
from ..models.security_price import SecurityPrice

class SecurityPriceQueries:
    @staticmethod
    def latest_price(db, security_id: int):
        return db.execute(
            select(SecurityPrice)
            .where(SecurityPrice.security_id == security_id)
            .order_by(SecurityPrice.trade_date.desc())
        ).scalars().first()

    @staticmethod
    def prices_for_range(db, security_id: int, start, end):
        return db.execute(
            select(SecurityPrice)
            .where(
                SecurityPrice.security_id == security_id,
                SecurityPrice.trade_date >= start,
                SecurityPrice.trade_date <= end,
            )
            .order_by(SecurityPrice.trade_date.asc())
        ).scalars().all()