from flask import Flask
from .config import get_config
from .db.session import init_request_scoped_session
from .routes.health_routes import bp as health_bp
from .routes.account_routes import bp as accounts_bp
from .routes.transaction_routes import bp as tx_bp
from .routes.portfolio_routes import bp as portfolio_bp
from .routes.dashboard_ui import bp as dashboard_ui
from .routes.accounts_ui import bp as accounts_ui

def create_app():
    cfg = get_config()

    app = Flask(__name__)
    app.config.from_object(cfg)

    # init request-scoped SQLAlchemy session
    init_request_scoped_session(app, cfg)

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
    app.register_blueprint(tx_bp, url_prefix="/api")
    app.register_blueprint(portfolio_bp, url_prefix="/api/portfolio")

    app.register_blueprint(dashboard_ui)
    app.register_blueprint(accounts_ui)
    return app