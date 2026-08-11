from datetime import datetime
from app.database import db

class InventoryHistory(db.Model):
    __tablename__ = 'inventory_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    change_type = db.Column(db.String(20), nullable=False) # 'Stock In', 'Stock Out', 'Adjustment', 'Sale', 'Sale Cancel'
    quantity_changed = db.Column(db.Integer, nullable=False)
    previous_stock = db.Column(db.Integer, nullable=True, default=0)
    remaining_quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    reference_code = db.Column(db.String(100), nullable=True, index=True)
    performed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', backref='inventory_actions', lazy=True)

    def get_reference(self) -> str:
        if self.reference_code:
            return self.reference_code
        return f"MANUAL-ADJ-{self.id:04d}"

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else '',
            'sku': self.product.sku if self.product else '',
            'change_type': self.change_type,
            'quantity_changed': self.quantity_changed,
            'previous_stock': self.previous_stock or 0,
            'remaining_quantity': self.remaining_quantity,
            'reason': self.reason or '',
            'remarks': self.remarks or '',
            'reference_code': self.get_reference(),
            'performed_by': self.user.full_name if self.user else 'System',
            'user_role': self.user.role if self.user else 'System',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }
