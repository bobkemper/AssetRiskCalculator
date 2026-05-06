from ..services.yahoo_security_service import YahooSecurityService
from ..services.yahoo_price_fetcher import YahooPriceFetcher
from ..services.security_service import SecurityService
from ..services.security_price_service import SecurityPriceService

class YahooIngestionService:
    @staticmethod
    def ingest_symbol(
        db,
        *,
        symbol: str,
        start=None,
        end=None
    ) -> dict:

        # 1) Fetch Yahoo security metadata
        sec_payload = YahooSecurityService.fetch_security_info(symbol)

        # 2) Create or get security
        existing = next(
            (s for s in SecurityService.list(db) if s.symbol == sec_payload["symbol"]),
            None
        )

        if existing:
            security = existing
        else:
            security = SecurityService.create(db, sec_payload)

        # 3) Fetch daily prices
        price_rows = YahooPriceFetcher.fetch_daily_prices(symbol, start, end)

        # 4) Store prices
        result = SecurityPriceService.bulk_insert_prices(
            db,
            security_id=security.id,
            rows=price_rows,
            source="yahoo",
            allow_update=False,
        )

        return {
            "security_id": security.id,
            "symbol": security.symbol,
            "prices_fetched": len(price_rows),
            **result,
        }
