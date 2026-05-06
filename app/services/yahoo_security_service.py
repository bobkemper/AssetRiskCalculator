import yfinance as yf

YAHOO_TYPE_MAP = {
    "EQUITY": "stock",
    "ETF": "etf",
    "MUTUALFUND": "mutual_fund",
    "CRYPTOCURRENCY": "crypto",
    "CURRENCY": "cash",
}

class YahooSecurityService:
    @staticmethod
    def fetch_security_info(symbol: str) -> dict:
        t = yf.Ticker(symbol)
        info = t.info  # dict from Yahoo [1](https://ranaroussi.github.io/yfinance/reference/yfinance.ticker_tickers.html)

        if not info:
            raise ValueError("No data returned from Yahoo")

        quote_type = info.get("quoteType")
        security_type = YAHOO_TYPE_MAP.get(quote_type, "custom")

        name = (
            info.get("longName")
            or info.get("shortName")
            or symbol
        )

        return {
            "symbol": symbol.upper(),
            "name": name,
            "security_type": security_type,
            "exchange": info.get("exchange"),
            "currency": info.get("currency", "USD"),
            "country": info.get("country"),
            "is_custom": False,
            "price_source": "yahoo",
            "external_id": symbol,
        }
