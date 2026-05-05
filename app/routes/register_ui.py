from datetime import date
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from ..db.session import get_session
from ..services.account_service import AccountService
from ..services.register_service import RegisterService
from ..constants import ENTRY_TYPE_LABELS, CASH_ENTRY_TYPES

bp = Blueprint("register_ui", __name__)

@bp.get("/accounts/<int:account_id>/register")
def show_register(account_id: int):
    db = get_session()
    account = AccountService.get_account(db, account_id)
    if not account:
        abort(404)

    rows = RegisterService.get_register_rows(db, account_id)
    current_balance = float(rows[-1].balance) if rows else 0.0

    # For now, show cash entry types for cash-like accounts;
    # later we’ll switch based on account.account_type.
    entry_types = [(k, ENTRY_TYPE_LABELS[k]) for k in CASH_ENTRY_TYPES]

    return render_template(
        "pages/register.html",
        account=account,
        rows=rows,
        current_balance=current_balance,
        entry_types=entry_types,
        today=date.today().isoformat(),
        entry_type_labels=ENTRY_TYPE_LABELS,
    )

@bp.post("/accounts/<int:account_id>/register")
def add_register_row(account_id: int):
    db = get_session()
    account = AccountService.get_account(db, account_id)
    if not account:
        abort(404)

    posted_date = request.form.get("posted_date")
    description = (request.form.get("description") or "").strip()
    entry_type = request.form.get("entry_type")

    debit_raw = (request.form.get("debit") or "").strip()
    credit_raw = (request.form.get("credit") or "").strip()

    # Basic validations
    if not posted_date:
        flash("Date is required.")
        return redirect(url_for("register_ui.show_register", account_id=account_id))

    if not description:
        flash("Description is required.")
        return redirect(url_for("register_ui.show_register", account_id=account_id))

    if entry_type not in CASH_ENTRY_TYPES:
        flash("Invalid entry type.")
        return redirect(url_for("register_ui.show_register", account_id=account_id))

    try:
        debit = Decimal(debit_raw) if debit_raw else None
        credit = Decimal(credit_raw) if credit_raw else None
    except InvalidOperation:
        flash("Debit/Credit must be valid numbers.")
        return redirect(url_for("register_ui.show_register", account_id=account_id))

    # enforce either debit or credit, not both (and not neither)
    if (debit is None and credit is None) or (debit is not None and credit is not None):
        flash("Enter either a Debit or a Credit (not both).")
        return redirect(url_for("register_ui.show_register", account_id=account_id))

    if debit is not None and debit <= 0:
        flash("Debit must be greater than zero.")
        return redirect(url_for("register_ui.show_register", account_id=account_id))

    if credit is not None and credit <= 0:
        flash("Credit must be greater than zero.")
        return redirect(url_for("register_ui.show_register", account_id=account_id))

    RegisterService.add_cash_entry(
        db=db,
        account_id=account_id,
        posted_date=posted_date,
        description=description,
        entry_type=entry_type,
        debit=debit,
        credit=credit,
    )

    flash("Entry added.")
    return redirect(url_for("register_ui.show_register", account_id=account_id))
