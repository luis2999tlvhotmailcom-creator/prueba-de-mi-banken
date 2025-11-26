from app import db

class PurchaseDetail(db.Model):
    __tablename__ = "PURCHASE_DETAIL"

    id = db.Column("identifier", db.Integer, primary_key=True)

    purchase_identifier = db.Column(
        db.Integer,
        db.ForeignKey("PURCHASES.identifier"),
        nullable=False
    )

    medication_identifier = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(7, 2), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(9, 2), nullable=False)

    # RELACIÓN DETALLE → CABECERA
    purchase = db.relationship("Purchase", back_populates="details")

    def to_dict(self):
        return {
            "id": self.id,
            "purchase_identifier": self.purchase_identifier,
            "medication_identifier": self.medication_identifier,
            "unit_price": float(self.unit_price),
            "amount": self.amount,
            "subtotal": float(self.subtotal)
        }
