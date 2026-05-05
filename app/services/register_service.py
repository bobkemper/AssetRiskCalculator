from decimal import Decimal
from sqlalchemy import select, func
from ..models.register_entry import RegisterEntry

class RegisterService:
    @staticmethod
    def add_opening_balance(db, account_id: int, posted_date, amount: Decimal):
        entry = RegisterEntry(
            account_id=account_id,
            posted_date=posted_date,
            description="Opening Balance",
            entry_type="opening",
            debit=None,
            credit=amount,
        )
        db.add(entry)
        db.flush()
        return entry

    @staticmethod
    def add_cash_entry(
        db,
        account_id: int,
        posted_date,
        description: str,
        entry_type: str,
        debit: Decimal | None,
        credit: Decimal | None,
    ):
        entry = RegisterEntry(
            account_id=account_id,
            posted_date=posted_date,
            description=description,
            entry_type=entry_type,
            debit=debit,
            credit=credit,
        )
        db.add(entry)
        db.flush()
        return entry

    @staticmethod
    def get_register_rows(db, account_id: int):
        net_amount = (
            func.coalesce(RegisterEntry.credit, 0)
            - func.coalesce(RegisterEntry.debit, 0)
        )

        running_balance = func.sum(net_amount).over(
            partition_by=RegisterEntry.account_id,
            order_by=[RegisterEntry.posted_date, RegisterEntry.id],
            rows=(None, 0),  # UNBOUNDED PRECEDING -> CURRENT ROW
        ).label("balance")

        stmt = (
            select(
                RegisterEntry.id,
                RegisterEntry.posted_date,
                RegisterEntry.description,
                RegisterEntry.entry_type,
                RegisterEntry.debit,
                RegisterEntry.credit,
                running_balance,
            )
            .where(RegisterEntry.account_id == account_id)
            .order_by(RegisterEntry.posted_date, RegisterEntry.id)
        )

        return db.execute(stmt).all()
