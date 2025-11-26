from app.models.delivery_detail import DeliveryDetail, db
from sqlalchemy.exc import IntegrityError

def listar_por_delivery(delivery_id):
    return DeliveryDetail.query.filter_by(delivery_identifier=delivery_id).all()

def crear(data):
    data["amount"] = data.get("amount", 0) or 0
    detail = DeliveryDetail(**data)
    db.session.add(detail)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")

    return detail

def eliminar(id):
    detail = DeliveryDetail.query.get(id)
    if not detail:
        return None

    db.session.delete(detail)
    db.session.commit()
    return detail
