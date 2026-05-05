from flask import Blueprint, request, jsonify
from ..db.session import get_session
from ..services.portfolio_service import PortfolioService

bp = Blueprint("portfolio", __name__)

@bp.get("/accounts/<int:account_id>/summary")
def summary(account_id: int):
    db = get_session()
    as_of = request.args.get("as_of_date")
    total_cost = PortfolioService.total_cost_basis(db, account_id, as_of_date=as_of)
    return jsonify({
        "account_id": account_id,
        "as_of_date": as_of,
        "total_cost_basis": total_cost
    })