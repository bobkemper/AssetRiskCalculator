from flask import Blueprint, render_template
from ..db.session import get_session
from ..services.account_service import AccountService

bp = Blueprint("dashboard_ui", __name__)

@bp.get("/")
def dashboard():
    db = get_session()
    accounts = AccountService.list_accounts(db)
    return render_template(
        "pages/dashboard.html",
        accounts=accounts
    )
