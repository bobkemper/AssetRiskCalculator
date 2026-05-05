from sqlalchemy import select, func
from ..models.position import Position

class PortfolioService:
    @staticmethod
    def total_cost_basis(db, account_id: int, as_of_date=None) -> float:
        stmt = select(func.coalesce(func.sum(Position.cost_basis_total), 0)).where(
            Position.account_id == account_id
        )
        if as_of_date:
            stmt = stmt.where(Position.as_of_date == as_of_date)
        return float(db.execute(stmt).scalar_one() or 0)
