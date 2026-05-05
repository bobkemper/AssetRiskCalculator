from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from ..db.session import get_session
from ..services.account_service import AccountService

from ..constants import ACCOUNT_TYPE_LABELS, TAX_TREATMENT_LABELS

bp = Blueprint("accounts_ui", __name__)



@bp.get("/accounts/<int:account_id>/edit")
def edit_account_form(account_id: int):
    db = get_session()
    account = AccountService.get_account(db, account_id)
    if not account:
        abort(404)

    return render_template(
        "pages/account_edit.html",
        account=account,
        account_types=ACCOUNT_TYPE_LABELS,
        tax_types=TAX_TREATMENT_LABELS,
    )


@bp.post("/accounts/<int:account_id>/edit")
def update_account(account_id: int):
    db = get_session()
    account = AccountService.get_account(db, account_id)
    if not account:
        abort(404)

    payload = {
        "name": request.form["name"].strip(),
        "institution": request.form.get("institution", "").strip(),
        "account_type": request.form["account_type"],
        "tax_treatment": request.form.get("tax_treatment") or None,
        "currency": request.form.get("currency", "USD"),
    }

    AccountService.update_account(db, account, payload)
    flash("Account updated")

    return redirect(url_for("accounts_ui.list_accounts"))


@bp.post("/accounts/<int:account_id>/delete")
def delete_account(account_id: int):
    db = get_session()
    account = AccountService.get_account(db, account_id)
    if not account:
        abort(404)

    AccountService.delete_account(db, account)
    flash("Account deleted")

    return redirect(url_for("accounts_ui.list_accounts"))

@bp.get("/accounts")
def list_accounts():
    db = get_session()
    accounts = AccountService.list_accounts(db)
    return render_template(
        "pages/accounts.html",
        accounts=accounts,
        account_type_labels=ACCOUNT_TYPE_LABELS,
        tax_types=TAX_TREATMENT_LABELS
    )


@bp.get("/accounts/new")
def new_account_form():
    return render_template("pages/account_new.html")


@bp.post("/accounts/new")
def create_account():
    db = get_session()
    payload = {
        "name": request.form.get("name", "").strip(),
        "institution": request.form.get("institution", "").strip(),
        "account_type": request.form.get("account_type"),
        "tax_treatment": request.form.get("tax_treatment") or None,
        "currency": request.form.get("currency", "USD"),
    }

    # Basic server-side validation
    if not payload["name"]:
        flash("Account name is required")
        return redirect(url_for("accounts_ui.new_account_form"))

    if not payload["account_type"]:
        flash("Account type is required")
        return redirect(url_for("accounts_ui.new_account_form"))

    AccountService.create_account(db, payload)
    flash("Account created successfully")

    return redirect(url_for("accounts_ui.list_accounts"))
