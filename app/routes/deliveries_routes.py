from flask import Blueprint, request, jsonify, send_file
from app.services import deliveries_service, delivery_detail_service

delivery_bp = Blueprint("deliveries", __name__)

# ============================
# CABECERA
# ============================

@delivery_bp.get("/<int:delivery_id>")
def get_by_id(delivery_id):
    delivery = deliveries_service.listar_por_id(delivery_id)
    if not delivery:
        return jsonify({"error": "Entrega no encontrada"}), 404
    return jsonify(delivery.to_dict()), 200


@delivery_bp.get("/")
def get_all():
    deliveries = deliveries_service.listar_todos()
    return jsonify([d.to_dict() for d in deliveries]), 200


@delivery_bp.post("/")
def create():
    data = request.get_json() or {}

    required = ["patient_identifier"]
    missing = [f for f in required if f not in data]

    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    data.pop("id", None)
    data.pop("delivery_date", None)

    try:
        delivery = deliveries_service.crear(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(delivery.to_dict()), 201


@delivery_bp.put("/<int:delivery_id>")
def update(delivery_id):
    data = request.get_json() or {}

    try:
        delivery = deliveries_service.editar(delivery_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not delivery:
        return jsonify({"error": "Entrega no encontrada"}), 404

    return jsonify(delivery.to_dict()), 200


# ============================
# ELIMINACIÓN LÓGICA
# ============================
@delivery_bp.patch("/delete/<int:delivery_id>")
def delete(delivery_id):
    delivery = deliveries_service.eliminar(delivery_id)
    if not delivery:
        return jsonify({"error": "Entrega no encontrada"}), 404
    return jsonify({"message": "Entrega desactivada"}), 200


# ============================
# RESTAURAR ENTREGA
# ============================
@delivery_bp.patch("/restore/<int:delivery_id>")
def restore(delivery_id):
    delivery = deliveries_service.restaurar(delivery_id)
    if not delivery:
        return jsonify({"error": "Entrega no encontrada"}), 404
    return jsonify({"message": "Entrega restaurada"}), 200


# ============================
# DETALLES
# ============================
@delivery_bp.get("/details/<int:delivery_id>")
def get_details(delivery_id):
    details = delivery_detail_service.listar_por_delivery(delivery_id)
    return jsonify([d.to_dict() for d in details]), 200


@delivery_bp.post("/details")
def create_detail():
    data = request.get_json() or {}

    required = ["delivery_identifier", "medication_identifier", "amount", "observations"]
    missing = [f for f in required if f not in data]

    if missing:
        return jsonify({"error": f"Faltan campos: {', '.join(missing)}"}), 400

    try:
        detail = delivery_detail_service.crear(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(detail.to_dict()), 201


@delivery_bp.delete("/details/<int:detail_id>")
def delete_detail(detail_id):
    detail = delivery_detail_service.eliminar(detail_id)
    if not detail:
        return jsonify({"error": "Detalle no encontrado"}), 404
    return jsonify({"message": "Detalle eliminado"}), 200


# ============================
# CREAR ENTREGAS + DETALLES (FULL)
# ============================
@delivery_bp.post("/full")
def create_full():
    data = request.get_json() or {}

    delivery_data = data.get("delivery")
    details_data = data.get("details", [])

    if not delivery_data or not details_data:
        return jsonify({"error": "Debe enviar 'delivery' y 'details'"}), 400

    try:
        # Pasar detalles al service
        delivery_data["details"] = details_data
        delivery = deliveries_service.crear(delivery_data)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(delivery.to_dict()), 201


# ============================
# REPORTES PDF / EXCEL
# ============================
@delivery_bp.get("/report/pdf/<int:delivery_id>")
def report_pdf(delivery_id):
    pdf_buffer = deliveries_service.generar_reporte_pdf(delivery_id)
    if not pdf_buffer:
        return jsonify({"error": "Entrega no encontrada"}), 404

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"delivery_{delivery_id}.pdf",
        mimetype="application/pdf"
    )


@delivery_bp.get("/report/excel/<int:delivery_id>")
def report_excel(delivery_id):
    excel_buffer = deliveries_service.generar_reporte_excel(delivery_id)
    if not excel_buffer:
        return jsonify({"error": "Entrega no encontrada"}), 404

    return send_file(
        excel_buffer,
        as_attachment=True,
        download_name=f"delivery_{delivery_id}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
