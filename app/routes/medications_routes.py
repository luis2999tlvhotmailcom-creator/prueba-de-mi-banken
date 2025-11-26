from flask import Blueprint, request, jsonify
from app.services import medications_service

medication_bp = Blueprint("medications", __name__)

@medication_bp.get("/")
def get_all():
    medications = medications_service.listar_todos()
    return jsonify([m.to_dict() for m in medications]), 200

@medication_bp.get("/<int:medication_id>")
def get_by_id(medication_id):
    medication = medications_service.listar_por_id(medication_id)
    if not medication:
        return jsonify({"error": "Medicamento no encontrado"}), 404
    return jsonify(medication.to_dict()), 200

@medication_bp.get("/estado/<string:estado>")
def get_by_estado(estado):
    medications = medications_service.listar_por_estado(estado)
    return jsonify([m.to_dict() for m in medications]), 200

@medication_bp.post("/")
def create():
    data = request.get_json() or {}

    required_fields = ["name", "batch_number", "stock", "minimum_stock", "expiration_date", "category", "medication_state"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400
    
    # 🔥 Evitar que envíen register_date manualmente
    data.pop("register_date", None)
    data.pop("id", None)  # Por seguridad, el id siempre debe ser automático

    try:
        medication = medications_service.crear(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify(medication.to_dict()), 201

@medication_bp.put("/<int:medication_id>")
def update(medication_id):
    data = request.get_json() or {}
    medication = medications_service.editar(medication_id, data)
    if not medication:
        return jsonify({"error": "Medicamento no encontrado"}), 404
    return jsonify(medication.to_dict()), 200

@medication_bp.patch("/eliminar/<int:medication_id>")
def eliminar(medication_id):
    medication = medications_service.eliminar_logico(medication_id)
    if not medication:
        return jsonify({"error": "Medicamento no encontrado"}), 404
    return jsonify(medication.to_dict()), 200

@medication_bp.patch("/restaurar/<int:medication_id>")
def restaurar(medication_id):
    medication = medications_service.restaurar_logico(medication_id)
    if not medication:
        return jsonify({"error": "Medicamento no encontrado"}), 404
    return jsonify(medication.to_dict()), 200
