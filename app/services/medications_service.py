from app.models.medications import Medication, db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# FUNCIONES DE CONSULTA

def listar_todos():
    return Medication.query.all()

def listar_por_id(id):
    return Medication.query.get(id)

def listar_por_estado(estado):
    return Medication.query.filter_by(medication_state=estado).all()


# CREAR NUEVO MEDICAMENTO

def crear(data):
    # Validar duplicado en batch_number antes de insertar
    if Medication.query.filter_by(batch_number=data.get("batch_number")).first():
        raise ValueError("El número de lote ya está registrado")

    # Convertir fecha si viene como string
    if "expiration_date" in data and isinstance(data["expiration_date"], str):
        try:
            data["expiration_date"] = datetime.strptime(data["expiration_date"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")

    # Crear instancia y guardar
    medication = Medication(**data)
    db.session.add(medication)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")
    return medication


# EDITAR MEDICAMENTO

def editar(id, data):
    medication = Medication.query.get(id)
    if not medication:
        return None

    # Validar duplicado en batch_number si lo están cambiando
    if "batch_number" in data and data["batch_number"] != medication.batch_number:
        if Medication.query.filter(
            Medication.batch_number == data["batch_number"],
            Medication.id != id
        ).first():
            raise ValueError("El número de lote ya está registrado")

    # Convertir fecha si viene como string
    if "expiration_date" in data and isinstance(data["expiration_date"], str):
        try:
            data["expiration_date"] = datetime.strptime(data["expiration_date"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD.")

    # Actualizar campos recibidos
    for key, value in data.items():
        setattr(medication, key, value)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")

    return medication


# ELIMINAR / RESTAURAR LÓGICO

def eliminar_logico(id):
    medication = Medication.query.get(id)
    if not medication:
        return None
    medication.medication_state = "I"  # I = Inactivo / Eliminado
    medication.stock = 0
    db.session.commit()
    return medication

def restaurar_logico(id):
    medication = Medication.query.get(id)
    if not medication:
        return None
    medication.medication_state = "A"  # A = Activo / Restaurado
    db.session.commit()
    return medication
