from flask import Blueprint, request, jsonify
from ..db.session import get_session
from ..services.security_service import SecurityService
from ..services.yahoo_ingestion_service import YahooIngestionService

bp = Blueprint("securities_api", __name__)

def _security_to_dict(s):
    return {
        "id": s.id,
        "symbol": s.symbol,
        "name": s.name,
        "security_type": s.security_type,
        "exchange": s.exchange,
        "currency": s.currency,
        "country": s.country,
        "is_custom": s.is_custom,
        "price_source": s.price_source,
        "external_id": s.external_id,
    }

@bp.get("/api/securities")
def list_securities():
    db = get_session()
    q = request.args.get("q")
    items = SecurityService.list(db, q=q)
    return jsonify([_security_to_dict(x) for x in items])

@bp.post("/api/securities")
def create_security():
    db = get_session()
    payload = request.json or {}
    try:
        s = SecurityService.create(db, payload)
        return jsonify({"ok": True, "security": _security_to_dict(s)})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@bp.put("/api/securities/<int:security_id>")
def update_security(security_id: int):
    db = get_session()
    payload = request.json or {}
    try:
        s = SecurityService.update(db, security_id, payload)
        return jsonify({"ok": True, "security": _security_to_dict(s)})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@bp.delete("/api/securities/<int:security_id>")
def delete_security(security_id: int):
    db = get_session()
    SecurityService.delete(db, security_id)
    return jsonify({"ok": True})

@bp.post("/api/yahoo/ingest")
def ingest_from_yahoo():
    db = get_session()
    payload = request.json or {}

    symbol = payload.get("symbol")
    start = payload.get("start")
    end = payload.get("end")

    if not symbol:
        return {"ok": False, "error": "symbol is required"}, 400

    result = YahooIngestionService.ingest_symbol(
        db,
        symbol=symbol,
        start=start,
        end=end
    )

    return {"ok": True, "result": result}