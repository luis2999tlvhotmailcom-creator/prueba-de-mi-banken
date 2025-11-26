from app import db
from sqlalchemy.sql import func

class Delivery(db.Model):
    __tablename__ = "DELIVERIES"

    id = db.Column("identifier", db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    patient_identifier = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False, default=0)
    notes = db.Column(db.String(120), nullable=False)
    delivery_state = db.Column(db.String(1), default="A", nullable=False)

    # CABECERA → DETALLE
    details = db.relationship(
        "DeliveryDetail",
        back_populates="delivery",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "delivery_date": str(self.delivery_date) if self.delivery_date else None,
            "patient_identifier": self.patient_identifier,
            "total_amount": self.total_amount,
            "notes": self.notes,
            "delivery_state": self.delivery_state,  # ← NUEVO
            "details": [d.to_dict() for d in self.details]
        }
