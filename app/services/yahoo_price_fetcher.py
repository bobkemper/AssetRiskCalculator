import yfinance as yf

class YahooPriceFetcher:
    @staticmethod
    def fetch_daily_prices(
        symbol: str,
        start=None,
        end=None
    ) -> list[dict]:
        t = yf.Ticker(symbol)

        df = t.history(
            start=start,
            end=end,
            interval="1d",
            auto_adjust=False
        )  # DataFrame with OHLCV + Adj Close [3](https://becomingquant.com/2026/01/23/pulling-historical-stock-data-with-yfinance-a-beginners-guide/)

        if df.empty:
            return []

        rows = []
        for idx, row in df.iterrows():
            rows.append({
                "trade_date": idx.date(),
                "open": float(row["Open"]) if not row["Open"] != row["Open"] else None,
                "high": float(row["High"]) if not row["High"] != row["High"] else None,
                "low": float(row["Low"]) if not row["Low"] != row["Low"] else None,
                "close": float(row["Close"]) if not row["Close"] != row["Close"] else None,
                "adj_close": float(row.get("Adj Close")) if "Adj Close" in row else None,
                "volume": int(row["Volume"]) if row["Volume"] == row["Volume"] else None,
            })

        return rows
