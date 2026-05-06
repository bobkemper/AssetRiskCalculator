from flask import Blueprint, request, jsonify
from datetime import date
from ..db.session import get_session
from ..services.portfolio_transaction_service import PortfolioTransactionService
from ..services.holdings_service import HoldingsService  # we’ll sketch below

bp = Blueprint("portfolio_transactions_api", __name__)

@bp.get("/api/portfolio/<int:portfolio_id>/transactions")
def list_transactions(portfolio_id):
    db = get_session()
    txs = PortfolioTransactionService.list_for_portfolio(db, portfolio_id)
    return jsonify([
        {
            "id": t.id,
            "portfolio_id": t.portfolio_id,
            "security_id": t.security_id,
            "transaction_type": t.transaction_type,
            "trade_date": t.trade_date.isoformat(),
            "quantity": float(t.quantity) if t.quantity is not None else None,
            "price": float(t.price) if t.price is not None else None,
            "cash_amount": float(t.cash_amount) if t.cash_amount is not None else None,
            "notes": t.notes,
        }
        for t in txs
    ])

@bp.post("/api/portfolio/<int:portfolio_id>/transactions")
def add_transaction(portfolio_id):
    db = get_session()
    payload = request.json or {}
    payload["portfolio_id"] = portfolio_id

    tx = PortfolioTransactionService.add_transaction(db, payload)
    db.commit()

    return {"ok": True, "id": tx.id}

@bp.get("/api/portfolio/<int:portfolio_id>/holdings")
def get_holdings(portfolio_id):
    db = get_session()
    rows = HoldingsService.current_holdings(db, portfolio_id)
    return jsonify(rows)
