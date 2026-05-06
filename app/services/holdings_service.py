from sqlalchemy import select, func, case
from ..models.portfolio_transaction import PortfolioTransaction
from ..models.security_price import SecurityPrice

class HoldingsService:
    @staticmethod
    def current_holdings(db, portfolio_id: int):
        # aggregate shares
        shares_subq = (
            select(
                PortfolioTransaction.security_id.label("security_id"),
                (
                    func.sum(
                        case(
                            (PortfolioTransaction.transaction_type == "BUY",
                             PortfolioTransaction.quantity),
                            (PortfolioTransaction.transaction_type == "SELL",
                             -PortfolioTransaction.quantity),
                            else_=0,
                        )
                    )
                ).label("shares")
            )
            .where(PortfolioTransaction.portfolio_id == portfolio_id)
            .group_by(PortfolioTransaction.security_id)
            .subquery()
        )

        # join latest prices
        latest_price_subq = (
            select(
                SecurityPrice.security_id,
                func.max(SecurityPrice.trade_date).label("max_date")
            )
            .group_by(SecurityPrice.security_id)
            .subquery()
        )

        q = (
            select(
                shares_subq.c.security_id,
                shares_subq.c.shares,
                SecurityPrice.close_price,
                (shares_subq.c.shares * SecurityPrice.close_price).label("market_value"),
            )
            .join(latest_price_subq,
                  latest_price_subq.c.security_id == shares_subq.c.security_id)
            .join(SecurityPrice,
                  (SecurityPrice.security_id == latest_price_subq.c.security_id) &
                  (SecurityPrice.trade_date == latest_price_subq.c.max_date))
            .where(shares_subq.c.shares != 0)
            .order_by(shares_subq.c.security_id)
        )

        return [
            {
                "security_id": r.security_id,
                "shares": float(r.shares),
                "price": float(r.close_price),
                "market_value": float(r.market_value),
            }
            for r in db.execute(q)
        ]
