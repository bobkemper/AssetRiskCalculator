from sqlalchemy import select, case
from sqlalchemy.exc import IntegrityError
from ..models.security import Security
from sqlalchemy import case


ALLOWED_SECURITY_TYPES = {
    "stock","etf","mutual_fund","crypto","cash","bond","custom"
}

ALLOWED_PRICE_SOURCES = {
    "manual","yahoo","alpha_vantage","none", None
}

class SecurityService:

   
    @staticmethod
    def list(db, *, q: str | None = None):
        stmt = select(Security)

        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                (Security.symbol.ilike(like)) |
                (Security.name.ilike(like))
            )

        stmt = stmt.order_by(
            Security.symbol.asc(),
            case(
                (Security.exchange.is_(None), 0),
                else_=1
            ),
            Security.exchange.asc(),
        )

        return db.execute(stmt).scalars().all()


    @staticmethod
    def get(db, security_id: int) -> Security | None:
        return db.get(Security, security_id)

    @staticmethod
    def create(db, payload: dict) -> Security:
        sym = (payload.get("symbol") or "").strip()
        name = (payload.get("name") or "").strip()
        sec_type = (payload.get("security_type") or "").strip()
        exch = (payload.get("exchange") or "").strip()
        curr = (payload.get("currency") or "USD").strip()
        country = (payload.get("country") or "").strip() or None
        is_custom = bool(payload.get("is_custom", False))
        price_source = payload.get("price_source", None)
        external_id = (payload.get("external_id") or "").strip() or None

        if not sym:
            raise ValueError("symbol is required")
        if not name:
            raise ValueError("name is required")
        if sec_type not in ALLOWED_SECURITY_TYPES:
            raise ValueError("invalid security_type")

        # Normalize for uniqueness and consistent lookup
        sym = sym.upper()
        exch = exch.upper() if exch else None
        curr = curr.upper()

        if price_source not in ALLOWED_PRICE_SOURCES:
            raise ValueError("invalid price_source")

        s = Security(
            symbol=sym,
            name=name,
            security_type=sec_type,
            exchange=exch,
            currency=curr,
            country=country,
            is_custom=is_custom,
            price_source=price_source,
            external_id=external_id,
        )
        db.add(s)
        try:
            db.flush()
        except IntegrityError as e:
            # likely duplicate symbol/exchange
            raise ValueError("Security already exists (symbol + exchange must be unique)") from e
        return s

    @staticmethod
    def update(db, security_id: int, payload: dict) -> Security:
        s = db.get(Security, security_id)
        if not s:
            raise ValueError("not found")

        # Allow updating metadata freely; be stricter later once prices/txns exist.
        if "name" in payload:
            s.name = (payload["name"] or "").strip()

        if "security_type" in payload:
            sec_type = (payload["security_type"] or "").strip()
            if sec_type not in ALLOWED_SECURITY_TYPES:
                raise ValueError("invalid security_type")
            s.security_type = sec_type

        if "exchange" in payload:
            exch = (payload["exchange"] or "").strip()
            s.exchange = exch.upper() if exch else None

        if "currency" in payload:
            curr = (payload["currency"] or "USD").strip()
            s.currency = curr.upper()

        if "country" in payload:
            c = (payload["country"] or "").strip()
            s.country = c or None

        if "is_custom" in payload:
            s.is_custom = bool(payload["is_custom"])

        if "price_source" in payload:
            ps = payload.get("price_source", None)
            if ps not in ALLOWED_PRICE_SOURCES:
                raise ValueError("invalid price_source")
            s.price_source = ps

        if "external_id" in payload:
            s.external_id = (payload["external_id"] or "").strip() or None

        # symbol update is risky — allow only for custom securities in v1
        if "symbol" in payload:
            new_sym = (payload["symbol"] or "").strip().upper()
            if not new_sym:
                raise ValueError("symbol cannot be blank")
            if not s.is_custom:
                raise ValueError("symbol can only be changed for custom securities")
            s.symbol = new_sym

        try:
            db.flush()
        except IntegrityError as e:
            raise ValueError("Security already exists (symbol + exchange must be unique)") from e

        return s

    @staticmethod
    def delete(db, security_id: int):
        s = db.get(Security, security_id)
        if not s:
            return
        # Later: prevent delete if referenced by prices/transactions
        db.delete(s)
