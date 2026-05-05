from app import create_app

app = create_app()

engine = app.extensions["db_engine"]

from app.db.init_db import create_all
create_all(engine)

print("Database tables created.")
