from flask import Blueprint, request, jsonify
from ..db.session import get_session
from ..services.account_service import AccountService

bp = Blueprint("accounts", __name__)

@bp.get("/")
def list_accounts():
    db = get_session()
    accounts = AccountService.list_accounts(db)
    return jsonify([{
        "id": a.id,
        "name": a.name,
        "institution": a.institution,
        "account_type": a.account_type,
        "tax_treatment": a.tax_treatment,
        "currency": a.currency
    } for a in accounts])

@bp.post("/")
def create_account():
    db = get_session()
    payload = request.get_json(force=True)
    acct = AccountService.create_account(db, payload)
    return jsonify({"id": acct.id}), 201