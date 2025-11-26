from app import db

class DeliveryDetail(db.Model):
    __tablename__ = "DELIVERY_DETAIL"

    id = db.Column("identifier", db.Integer, primary_key=True)

    delivery_identifier = db.Column(
        db.Integer,
        db.ForeignKey("DELIVERIES.identifier"),
        nullable=False
    )

    medication_identifier = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    observations = db.Column(db.String(120), nullable=False)

    # RELACIÓN DETALLE → CABECERA
    delivery = db.relationship("Delivery", back_populates="details")

    def to_dict(self):
        return {
            "id": self.id,
            "delivery_identifier": self.delivery_identifier,
            "medication_identifier": self.medication_identifier,
            "amount": self.amount,
            "observations": self.observations
        }
