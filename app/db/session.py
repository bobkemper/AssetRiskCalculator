from flask import g
from sqlalchemy.orm import sessionmaker
from .engine import make_engine

def init_request_scoped_session(app, cfg):
    engine = make_engine(cfg)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    app.extensions["db_engine"] = engine
    app.extensions["SessionLocal"] = SessionLocal

    @app.before_request
    def _open_session():
        g.db = SessionLocal()

    @app.teardown_request
    def _close_session(exc):
        db = getattr(g, "db", None)
        if db is None:
            return
        try:
            if exc is None:
                db.commit()
            else:
                db.rollback()
        finally:
            db.close()

def get_session():
    return g.db
