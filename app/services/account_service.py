from sqlalchemy import select
from ..models.account import Account

class AccountService:
    @staticmethod
    def list_accounts(db):
        return db.execute(select(Account).order_by(Account.name.asc())).scalars().all()

    @staticmethod
    def create_account(db, payload: dict) -> Account:
        acct = Account(
            name=payload["name"],
            institution=payload.get("institution"),
            account_type=payload["account_type"],
            tax_treatment=payload.get("tax_treatment"),
            currency=payload.get("currency", "USD"),
        )
        db.add(acct)
        db.flush()
        return acct
