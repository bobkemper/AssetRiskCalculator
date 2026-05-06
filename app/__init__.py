from flask import Flask
from .config import get_config
from .db.session import init_request_scoped_session
from .routes.health_routes import bp as health_bp
from .routes.account_routes import bp as accounts_bp
from .routes.transaction_routes import bp as tx_bp
from .routes.portfolio_routes import bp as portfolio_bp
from .routes.dashboard_ui import bp as dashboard_ui
from .routes.accounts_ui import bp as accounts_ui
from .routes.register_ui import bp as register_ui
from .routes.register_api import bp as register_api
from .routes.securities_api import bp as securities_api
from .routes.securities_ui import bp as securities_ui
from .routes.yahoo_ingestion_ui import bp as yahoo_ingestion_ui
from .routes.portfolio_transactions_api import bp as portfolio_transactions_api
from .routes.portfolio_ui import bp as portfolio_ui

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
    app.register_blueprint(register_ui)
    app.register_blueprint(register_api)
    app.register_blueprint(securities_api)
    app.register_blueprint(securities_ui)
    app.register_blueprint(yahoo_ingestion_ui)
    app.register_blueprint(portfolio_transactions_api)
    app.register_blueprint(portfolio_ui)

    return app