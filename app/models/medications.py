from app import db
from sqlalchemy.sql import func

class Medication(db.Model):
    __tablename__ = "MEDICATIONS"

    id = db.Column("identifier", db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    batch_number = db.Column(db.String(12), unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    minimum_stock = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(10), nullable=False)
    medication_state = db.Column(db.String(1), nullable=False)
    register_date = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "batch_number": self.batch_number,
            "stock": self.stock,
            "minimum_stock": self.minimum_stock,
            "expiration_date": str(self.expiration_date) if self.expiration_date else None,
            "category": self.category,
            "medication_state": self.medication_state,
            "register_date": str(self.register_date) if self.register_date else None,
        }
