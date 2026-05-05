from sqlalchemy import select
from ..models.transaction import Transaction

class TransactionService:
    @staticmethod
    def list_for_account(db, account_id: int):
        stmt = (select(Transaction)
                .where(Transaction.account_id == account_id)
                .order_by(Transaction.posted_date.desc(), Transaction.id.desc()))
        return db.execute(stmt).scalars().all()

    @staticmethod
    def add_transaction(db, account_id: int, payload: dict) -> Transaction:
        tx = Transaction(
            account_id=account_id,
            posted_date=payload["posted_date"],
            description=payload["description"],
            amount=payload["amount"],
            category=payload.get("category"),
            memo=payload.get("memo"),
        )
        db.add(tx)
        db.flush()
        return tx
