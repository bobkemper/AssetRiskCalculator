from flask import Blueprint, render_template
from ..db.session import get_session
from ..services.account_service import AccountService
from ..services.transaction_service import TransactionService

bp = Blueprint("accounts_ui", __name__)

@bp.get("/accounts")
def list_accounts():
    db = get_session()
    accounts = AccountService.list_accounts(db)
    return render_template(
        "pages/accounts.html",
        accounts=accounts
    )

@bp.get("/accounts/<int:account_id>")
def account_detail(account_id: int):
    db = get_session()
    txs = TransactionService.list_for_account(db, account_id)
    return render_template(
        "pages/account_detail.html",
        transactions=txs
    )
