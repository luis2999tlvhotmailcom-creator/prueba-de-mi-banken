from flask import Blueprint, request, jsonify
from app.services import purchase_detail_service

purchase_detail_bp = Blueprint("purchase_detail", __name__)

@purchase_detail_bp.get("/purchase/<int:purchase_id>", endpoint="get_details_by_purchase")
def get_by_purchase(purchase_id):
    details = purchase_detail_service.listar_por_purchase(purchase_id)
    return jsonify([d.to_dict() for d in details]), 200

@purchase_detail_bp.post("/", endpoint="create_purchase_detail")
def create():
    data = request.get_json() or {}

    required = ["purchase_identifier", "medication_identifier", "unit_price", "amount", "subtotal"]
    missing = [f for f in required if f not in data]

    if missing:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing)}"}), 400

    try:
        detail = purchase_detail_service.crear(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(detail.to_dict()), 201

@purchase_detail_bp.delete("/<int:detail_id>", endpoint="delete_purchase_detail")
def delete(detail_id):
    detail = purchase_detail_service.eliminar(detail_id)
    if not detail:
        return jsonify({"error": "Detalle no encontrado"}), 404

    return jsonify({"message": "Detalle eliminado"}), 200
