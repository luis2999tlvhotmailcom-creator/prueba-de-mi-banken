from flask import Blueprint, request, jsonify
from app.services import suppliers_service

supplier_bp = Blueprint("suppliers", __name__)

# ✅ ELIMINAR TODAS LAS RUTAS OPTIONS - ahora se manejan globalmente

# ✅ PRIMERO las rutas MÁS ESPECÍFICAS (con parámetros)
@supplier_bp.get("/estado/<string:estado>", endpoint="get_suppliers_by_status")
def get_by_estado(estado):
    suppliers = suppliers_service.listar_por_estado(estado)
    return jsonify([s.to_dict() for s in suppliers]), 200

@supplier_bp.get("/<int:supplier_id>", endpoint="get_supplier_by_id")
def get_by_id(supplier_id):
    supplier = suppliers_service.listar_por_id(supplier_id)
    if not supplier:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    return jsonify(supplier.to_dict()), 200

@supplier_bp.put("/<int:supplier_id>", endpoint="update_supplier")
def update(supplier_id):
    data = request.get_json() or {}
    try:
        supplier = suppliers_service.editar(supplier_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not supplier:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    return jsonify(supplier.to_dict()), 200

@supplier_bp.patch("/eliminar/<int:supplier_id>", endpoint="soft_delete_supplier")
def eliminar(supplier_id):
    supplier = suppliers_service.eliminar_logico(supplier_id)
    if not supplier:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    return jsonify(supplier.to_dict()), 200

@supplier_bp.patch("/restaurar/<int:supplier_id>", endpoint="restore_supplier")
def restaurar(supplier_id):
    supplier = suppliers_service.restaurar_logico(supplier_id)
    if not supplier:
        return jsonify({"error": "Proveedor no encontrado"}), 404
    return jsonify(supplier.to_dict()), 200

# ✅ LUEGO las rutas GENERALES (sin parámetros)
@supplier_bp.get("/", endpoint="get_all_suppliers")
def get_all():
    suppliers = suppliers_service.listar_todos()
    return jsonify([s.to_dict() for s in suppliers]), 200

# ✅ POR ÚLTIMO la ruta POST (ruta general)
@supplier_bp.post("/", endpoint="create_supplier")
def create():
    data = request.get_json() or {}
    print("🎯 DATOS RECIBIDOS EN BACKEND:", data)

    required_fields = ["company_name", "ruc", "phone", "email", "supplier_state"]
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

    data.pop("register_date", None)
    data.pop("id", None)

    try:
        supplier = suppliers_service.crear(data)
        print("✅ PROVEEDOR CREADO:", supplier.to_dict())
    except ValueError as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 400

    return jsonify(supplier.to_dict()), 201
