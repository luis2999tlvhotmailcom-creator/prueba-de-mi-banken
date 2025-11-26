from app.models.suppliers import Supplier, db
from sqlalchemy.exc import IntegrityError

def listar_todos():
    return Supplier.query.all()

def listar_por_id(id):
    return Supplier.query.get(id)

def listar_por_estado(estado):
    return Supplier.query.filter_by(supplier_state=estado).all()

def crear(data):
    # Validar duplicado de RUC antes de insertar
    if Supplier.query.filter_by(ruc=data.get("ruc")).first():
        raise ValueError("El RUC ya está registrado")

    # Validar duplicado de email (opcional, pero recomendable)
    if Supplier.query.filter_by(email=data.get("email")).first():
        raise ValueError("El email ya está registrado")

    supplier = Supplier(**data)
    db.session.add(supplier)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")
    return supplier

def editar(id, data):
    supplier = Supplier.query.get(id)
    if not supplier:
        return None

    # Validar duplicado de RUC si lo están modificando
    if "ruc" in data and data["ruc"] != supplier.ruc:
        if Supplier.query.filter(
            Supplier.ruc == data["ruc"],
            Supplier.id != id
        ).first():
            raise ValueError("El RUC ya está registrado")

    # Validar duplicado de email si lo están modificando
    if "email" in data and data["email"] != supplier.email:
        if Supplier.query.filter(
            Supplier.email == data["email"],
            Supplier.id != id
        ).first():
            raise ValueError("El email ya está registrado")

    # Actualizar todos los campos recibidos en data
    for key, value in data.items():
        setattr(supplier, key, value)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")

    return supplier

def eliminar_logico(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return None
    supplier.supplier_state = "I"  # I = Inactivo / Eliminado
    db.session.commit()
    return supplier

def restaurar_logico(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return None
    supplier.supplier_state = "A"  # A = Activo / Restaurado
    db.session.commit()
    return supplier
