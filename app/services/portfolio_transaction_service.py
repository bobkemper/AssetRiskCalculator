from sqlalchemy import select
from ..models.portfolio_transaction import PortfolioTransaction

class PortfolioTransactionService:
    @staticmethod
    def add_transaction(db, payload: dict) -> PortfolioTransaction:
        tx = PortfolioTransaction(
            portfolio_id=payload["portfolio_id"],
            security_id=payload.get("security_id"),
            transaction_type=payload["transaction_type"],
            trade_date=payload["trade_date"],
            quantity=payload.get("quantity"),
            price=payload.get("price"),
            cash_amount=payload.get("cash_amount"),
            currency=payload.get("currency", "USD"),
            notes=payload.get("notes"),
        )
        db.add(tx)
        db.flush()
        return tx

    @staticmethod
    def list_for_portfolio(db, portfolio_id: int):
        return db.execute(
            select(PortfolioTransaction)
            .where(PortfolioTransaction.portfolio_id == portfolio_id)
            .order_by(
                PortfolioTransaction.trade_date.asc(),
                PortfolioTransaction.id.asc(),
            )
        ).scalars().all()
