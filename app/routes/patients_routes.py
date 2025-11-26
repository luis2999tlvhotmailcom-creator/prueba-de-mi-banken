from flask import Blueprint, request, jsonify
from app.services import patients_service

patient_bp = Blueprint("patients", __name__, url_prefix="/patients")

# ==============================
# CONSULTAS
# ==============================

@patient_bp.get("/")
def get_all():
    patients = patients_service.listar_todos()
    return jsonify([p.to_dict() for p in patients]), 200

@patient_bp.get("/<int:patient_id>")
def get_by_id(patient_id):
    patient = patients_service.listar_por_id(patient_id)
    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404
    return jsonify(patient.to_dict()), 200

@patient_bp.get("/dni/<string:dni>")
def get_by_dni(dni):
    patient = patients_service.listar_por_dni(dni)
    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404
    return jsonify(patient.to_dict()), 200

@patient_bp.get("/estado/<string:estado>")
def get_by_estado(estado):
    patients = patients_service.listar_por_estado(estado)
    return jsonify([p.to_dict() for p in patients]), 200


# ==============================
# CREAR
# ==============================

@patient_bp.post("/")
def create():
    data = request.get_json() or {}

    required_fields = ["dni", "name", "last_name", "age", "gender", "phone", "email", "patient_state"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing)}"}), 400

    data.pop("id", None)

    try:
        patient = patients_service.crear(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(patient.to_dict()), 201


# ==============================
# EDITAR
# ==============================

@patient_bp.put("/<int:patient_id>")
def update(patient_id):
    data = request.get_json() or {}
    try:
        patient = patients_service.editar(patient_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404

    return jsonify(patient.to_dict()), 200


# ==============================
# ELIMINAR / RESTAURAR LÓGICO
# ==============================

@patient_bp.patch("/eliminar/<int:patient_id>")
def eliminar(patient_id):
    patient = patients_service.eliminar_logico(patient_id)
    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404
    return jsonify(patient.to_dict()), 200

@patient_bp.patch("/restaurar/<int:patient_id>")
def restaurar(patient_id):
    patient = patients_service.restaurar_logico(patient_id)
    if not patient:
        return jsonify({"error": "Paciente no encontrado"}), 404
    return jsonify(patient.to_dict()), 200
