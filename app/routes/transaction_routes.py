from flask import Blueprint, request, jsonify
from ..db.session import get_session
from ..services.transaction_service import TransactionService

bp = Blueprint("transactions", __name__)

@bp.get("/accounts/<int:account_id>/transactions")
def list_transactions(account_id: int):
    db = get_session()
    txs = TransactionService.list_for_account(db, account_id)
    return jsonify([{
        "id": t.id,
        "posted_date": t.posted_date.isoformat(),
        "description": t.description,
        "amount": float(t.amount),
        "category": t.category,
        "memo": t.memo
    } for t in txs])

@bp.post("/accounts/<int:account_id>/transactions")
def add_transaction(account_id: int):
    db = get_session()
    payload = request.get_json(force=True)
    tx = TransactionService.add_transaction(db, account_id, payload)
    return jsonify({"id": tx.id}), 201