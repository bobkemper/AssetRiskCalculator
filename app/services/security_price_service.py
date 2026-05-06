from sqlalchemy import select, tuple_
from ..models.security_price import SecurityPrice

class SecurityPriceService:
    @staticmethod
    def bulk_insert_prices(
        db,
        *,
        security_id: int,
        rows: list[dict],
        source: str,
        allow_update: bool = False,
    ) -> dict:

        if not rows:
            return {"inserted": 0, "updated": 0}

        dates = [r["trade_date"] for r in rows]
        min_date = min(dates)
        max_date = max(dates)

        # ✅ SQL Server–safe existence check
        existing = set(
            db.execute(
                select(SecurityPrice.trade_date).where(
                    SecurityPrice.security_id == security_id,
                    SecurityPrice.trade_date >= min_date,
                    SecurityPrice.trade_date <= max_date,
                )
            ).scalars().all()
        )

        to_insert = []
        to_update = []

        for r in rows:
            if r["trade_date"] in existing:
                if allow_update:
                    to_update.append(r)
            else:
                to_insert.append(SecurityPrice(
                    security_id=security_id,
                    trade_date=r["trade_date"],
                    open_price=r.get("open"),
                    high_price=r.get("high"),
                    low_price=r.get("low"),
                    close_price=r.get("close"),
                    adjusted_close=r.get("adj_close"),
                    volume=r.get("volume"),
                    source=source,
                ))

        if to_insert:
            db.add_all(to_insert)

        if allow_update and to_update:
            for r in to_update:
                db.execute(
                    db.update(SecurityPrice)
                    .where(
                        SecurityPrice.security_id == security_id,
                        SecurityPrice.trade_date == r["trade_date"],
                    )
                    .values(
                        open_price=r.get("open"),
                        high_price=r.get("high"),
                        low_price=r.get("low"),
                        close_price=r.get("close"),
                        adjusted_close=r.get("adj_close"),
                        volume=r.get("volume"),
                        source=source,
                    )
                )

        return {
            "inserted": len(to_insert),
            "updated": len(to_update),
        }