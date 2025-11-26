from app import db
from sqlalchemy.sql import func

class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column("identifier", db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    ruc = db.Column(db.String(11), nullable=False, unique=True)
    phone = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    supplier_state = db.Column(db.String(1), nullable=False)
    register_date = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "ruc": self.ruc,
            "phone": self.phone,
            "email": self.email,
            "supplier_state": self.supplier_state,
            "register_date": str(self.register_date) if self.register_date else None,
        }
