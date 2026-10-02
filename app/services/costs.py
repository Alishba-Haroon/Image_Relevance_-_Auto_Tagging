from sqlalchemy.orm import Session
from app.models.entities import CostLog

def record_cost(db: Session, operation: str, item_id: str, estimated_cost_usd: float = 0.0):
    db.add(CostLog(
        operation=operation,
        item_id=item_id,
        estimated_cost_usd=estimated_cost_usd,
    ))
    db.commit()
