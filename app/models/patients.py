from app import db

class Patient(db.Model):
    __tablename__ = "PATIENTS"

    id = db.Column("identifier", db.Integer, primary_key=True)
    dni = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    phone = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    patient_state = db.Column(db.String(1), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "dni": self.dni,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "patient_state": self.patient_state,
        }
