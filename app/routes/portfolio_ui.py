from flask import Blueprint, render_template

bp = Blueprint("portfolio_ui", __name__)

@bp.get("/portfolio/<int:portfolio_id>")
def portfolio_screen(portfolio_id):
    return render_template(
        "pages/portfolio.html",
        portfolio_id=portfolio_id,
    )
