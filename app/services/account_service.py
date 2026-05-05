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

    @staticmethod
    def get_account(db, account_id: int) -> Account | None:
        return db.execute(
            select(Account).where(Account.id == account_id)
        ).scalar_one_or_none()

    @staticmethod
    def update_account(db, account: Account, payload: dict):
        account.name = payload["name"]
        account.institution = payload.get("institution")
        account.account_type = payload["account_type"]
        account.tax_treatment = payload.get("tax_treatment")
        account.currency = payload.get("currency", "USD")

    @staticmethod
    def delete_account(db, account: Account):
        db.delete(account)

