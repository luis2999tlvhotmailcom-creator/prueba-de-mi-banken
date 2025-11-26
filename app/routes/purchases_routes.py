from flask import Blueprint, request, jsonify, send_file
from app.services import purchase_detail_service, purchases_service

purchase_bp = Blueprint("purchases", __name__)

# ============================
# RUTAS CON PARÁMETROS
# ============================

@purchase_bp.get("/<int:purchase_id>", endpoint="get_purchase_by_id")
def get_by_id(purchase_id):
    purchase = purchases_service.listar_por_id(purchase_id)
    if not purchase:
        return jsonify({"error": "Compra no encontrada"}), 404
    return jsonify(purchase.to_dict()), 200


@purchase_bp.put("/<int:purchase_id>", endpoint="update_purchase")
def update(purchase_id):
    data = request.get_json() or {}

    try:
        purchase = purchases_service.editar(purchase_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not purchase:
        return jsonify({"error": "Compra no encontrada"}), 404

    return jsonify(purchase.to_dict()), 200


@purchase_bp.patch("/delete/<int:purchase_id>", endpoint="delete_purchase")
def delete(purchase_id):
    purchase = purchases_service.eliminar(purchase_id)
    if not purchase:
        return jsonify({"error": "Compra no encontrada"}), 404
    return jsonify({"message": "Compra desactivada correctamente"}), 200


@purchase_bp.patch("/restore/<int:purchase_id>", endpoint="restore_purchase")
def restore(purchase_id):
    purchase = purchases_service.restaurar(purchase_id)
    if not purchase:
        return jsonify({"error": "Compra no encontrada"}), 404
    return jsonify({"message": "Compra restaurada correctamente"}), 200


# ============================
# RUTAS GENERALES
# ============================

@purchase_bp.get("/", endpoint="get_all_purchases")
def get_all():
    purchases = purchases_service.listar_todos()
    return jsonify([p.to_dict() for p in purchases]), 200


@purchase_bp.post("/", endpoint="create_purchase")
def create():
    data = request.get_json() or {}

    required = ["supplier_identifier", "total_amount", "total_price"]
    missing = [f for f in required if f not in data]

    if missing:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing)}"}), 400

    data.pop("id", None)
    data.pop("purchase_date", None)

    try:
        purchase = purchases_service.crear(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(purchase.to_dict()), 201


@purchase_bp.post("/full", endpoint="create_purchase_with_details")
def create_full():
    data = request.get_json() or {}

    purchase_data = data.get("purchase")
    details_data = data.get("details", [])

    if not purchase_data or not details_data:
        return jsonify({"error": "Debe enviar 'purchase' y 'details'"}), 400

    purchase = purchases_service.crear(purchase_data)

    for detail in details_data:
        detail["purchase_identifier"] = purchase.id
        purchase_detail_service.crear(detail)

    return jsonify(purchase.to_dict()), 201


# ============================================
# REPORTES
# ============================================

@purchase_bp.get("/report/pdf/<int:purchase_id>", endpoint="purchase_pdf_report")
def report_pdf(purchase_id):
    pdf_buffer = purchases_service.generar_reporte_pdf(purchase_id)

    if not pdf_buffer:
        return jsonify({"error": "Compra no encontrada"}), 404

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"purchase_{purchase_id}.pdf",
        mimetype="application/pdf"
    )


@purchase_bp.get("/report/excel/<int:purchase_id>", endpoint="purchase_excel_report")
def report_excel(purchase_id):
    excel_buffer = purchases_service.generar_reporte_excel(purchase_id)

    if not excel_buffer:
        return jsonify({"error": "Compra no encontrada"}), 404

    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name=f"purchase_{purchase_id}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
