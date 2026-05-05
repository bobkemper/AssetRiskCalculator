import os
# app/config.py

class BaseConfig:
    SECRET_KEY = "dev"

    DB_SERVER = "localhost"
    DB_NAME = "pfinance"
    DB_USER = "finance_admin"
    DB_PASSWORD = "P@ssw0rd!"
    DB_DRIVER = "ODBC Driver 17 for SQL Server"



def get_config():
    return BaseConfig()  # ✅ INSTANCE, not class

