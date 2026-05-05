from .base import Base

def create_all(engine):
    # ensure models are loaded
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)