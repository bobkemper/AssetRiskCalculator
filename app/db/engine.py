import urllib.parse
from sqlalchemy import create_engine

def build_sqlalchemy_url(cfg) -> str:
    extra = ""
    if extra and not extra.endswith(";"):
        extra += ";"

    odbc_str = (
        f"DRIVER={cfg.DB_DRIVER};"
        f"SERVER={cfg.DB_SERVER};"
        f"DATABASE={cfg.DB_NAME};"
        f"UID={cfg.DB_USER};"
        f"PWD={cfg.DB_PASSWORD};"
        f"{extra}"
    )

    params = urllib.parse.quote_plus(odbc_str)
    return f"mssql+pyodbc:///?odbc_connect={params}"  # SQLAlchemy SQL Server dialect [4](https://docs.sqlalchemy.org/en/14/dialects/mssql.html)



def make_engine(cfg):
    url = build_sqlalchemy_url(cfg)
    return create_engine(
        url,
        pool_pre_ping=True,   # helps with stale pooled connections
        future=True
    )