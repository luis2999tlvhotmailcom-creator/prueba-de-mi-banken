from app import db
from sqlalchemy.sql import func

class Purchase(db.Model):
    __tablename__ = "PURCHASES"

    id = db.Column("identifier", db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    supplier_identifier = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(9, 2), nullable=False)
    purchase_state = db.Column(db.String(1), default="A", nullable=False)

    # CABECERA → DETALLE
    details = db.relationship(
        "PurchaseDetail",
        back_populates="purchase",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "purchase_date": str(self.purchase_date) if self.purchase_date else None,
            "supplier_identifier": self.supplier_identifier,
            "total_amount": self.total_amount,
            "total_price": float(self.total_price),
            "purchase_state": self.purchase_state,
            "details": [d.to_dict() for d in self.details]
        }
