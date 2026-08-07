from datetime import datetime
from app.database import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    total_purchases = db.Column(db.Float, default=0.0)
    outstanding_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), nullable=False, default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bills = db.relationship('Bill', backref='customer', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email or '',
            'address': self.address or '',
            'total_purchases': self.total_purchases,
            'outstanding_amount': self.outstanding_amount,
            'status': self.status,
            'bill_count': len(self.bills) if self.bills else 0,
            'created_at': self.created_at.strftime('%Y-%m-%d') if self.created_at else ''
        }
