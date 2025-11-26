from app import db
from app.models.patients import Patient
from sqlalchemy.exc import IntegrityError

# ==============================
# CONSULTAS
# ==============================

def listar_todos():
    return Patient.query.all()

def listar_por_id(id):
    return Patient.query.get(id)

def listar_por_estado(estado):
    return Patient.query.filter_by(patient_state=estado).all()

def listar_por_dni(dni):
    return Patient.query.filter_by(dni=dni).first()


# ==============================
# CREAR PACIENTE
# ==============================

def crear(data):
    # Validar duplicado por DNI
    if Patient.query.filter_by(dni=data.get("dni")).first():
        raise ValueError("El DNI ya está registrado")

    patient = Patient(**data)
    db.session.add(patient)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")

    return patient


# ==============================
# EDITAR PACIENTE
# ==============================

def editar(id, data):
    patient = Patient.query.get(id)
    if not patient:
        return None

    # Validar duplicado de DNI si lo cambian
    if "dni" in data and data["dni"] != patient.dni:
        if Patient.query.filter(
            Patient.dni == data["dni"],
            Patient.id != id
        ).first():
            raise ValueError("El DNI ya está registrado")

    # Actualizar campos
    for key, value in data.items():
        setattr(patient, key, value)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error de integridad: {str(e)}")

    return patient


# ==============================
# ELIMINAR / RESTAURAR LÓGICO
# ==============================

def eliminar_logico(id):
    patient = Patient.query.get(id)
    if not patient:
        return None
    patient.patient_state = "I"
    db.session.commit()
    return patient

def restaurar_logico(id):
    patient = Patient.query.get(id)
    if not patient:
        return None
    patient.patient_state = "A"
    db.session.commit()
    return patient
