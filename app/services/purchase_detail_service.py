from app.models.purchase_detail import PurchaseDetail, db
from sqlalchemy.exc import IntegrityError

def listar_por_purchase(purchase_id):
    return PurchaseDetail.query.filter_by(purchase_identifier=purchase_id).all()

def crear(data):
    detail = PurchaseDetail(**data)
    db.session.add(detail)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")

    return detail

def eliminar(id):
    detail = PurchaseDetail.query.get(id)
    if not detail:
        return None

    db.session.delete(detail)
    db.session.commit()
    return detail
