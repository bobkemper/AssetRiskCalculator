from decimal import Decimal
from flask import Blueprint, request, jsonify, abort
from ..db.session import get_session
from ..services.account_service import AccountService
from ..services.register_service import RegisterService
from ..models.register_entry import RegisterEntry
from decimal import Decimal
from datetime import date

bp = Blueprint("register_api", __name__)

@bp.get("/api/accounts/<int:account_id>/register")
def api_get_register(account_id: int):
    db = get_session()
    account = AccountService.get_account(db, account_id)
    if not account:
        abort(404)

    rows = RegisterService.get_register_rows(db, account_id)

    return jsonify([
        {
            "id": r.id,
            "posted_date": r.posted_date.isoformat(),
            "description": r.description,
            "entry_type": r.entry_type,
            "debit": float(r.debit) if r.debit else None,
            "credit": float(r.credit) if r.credit else None,
            "balance": float(r.balance),
        }
        for r in rows
    ])

@bp.post("/api/accounts/<int:account_id>/register")
def api_add_register_row(account_id: int):
    db = get_session()
    data = request.json or {}

    entry = RegisterService.add_cash_entry(
        db=db,
        account_id=account_id,
        posted_date=parse_date(data["posted_date"]),
        description=data["description"],
        entry_type=data["entry_type"],
        debit=dec_or_none(data.get("debit")),
        credit=dec_or_none(data.get("credit")),
    )

    return jsonify({"ok": True, "id": entry.id})


@bp.put("/api/register/<int:entry_id>")
def api_update_register_row(entry_id: int):
    db = get_session()
    entry = db.get(RegisterEntry, entry_id)
    if not entry:
        abort(404)

    data = request.json or {}

    entry.posted_date = parse_date(data["posted_date"])
    entry.description = data["description"]
    entry.entry_type = data["entry_type"]
  
    entry.debit = dec_or_none(data.get("debit"))
    entry.credit = dec_or_none(data.get("credit"))

    return jsonify({"ok": True})


@bp.delete("/api/register/<int:entry_id>")
def api_delete_register_row(entry_id: int):
    db = get_session()
    entry = db.get(RegisterEntry, entry_id)
    if not entry:
        abort(404)

    db.delete(entry)
    return {"ok": True}

def dec_or_none(v):
    return Decimal(str(v)) if v is not None else None

def parse_date(s: str) -> date:
    # expects 'YYYY-MM-DD'
    return date.fromisoformat(s)