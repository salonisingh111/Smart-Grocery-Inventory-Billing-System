from datetime import datetime
from app.database import db

class Bill(db.Model):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    tax_amount = db.Column(db.Float, nullable=False, default=0.0)
    discount_amount = db.Column(db.Float, nullable=False, default=0.0)
    round_off = db.Column(db.Float, nullable=False, default=0.0)
    net_amount = db.Column(db.Float, nullable=False, default=0.0)
    
    payment_method = db.Column(db.String(30), nullable=False, default='Cash') # Cash, UPI, Card
    status = db.Column(db.String(20), nullable=False, default='Paid') # Paid, Cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    items = db.relationship('BillItem', backref='bill', lazy=True, cascade="all, delete-orphan")
    user = db.relationship('User', backref='bills', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'bill_number': self.bill_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else 'Walk-in Customer',
            'customer_phone': self.customer.phone if self.customer else '',
            'user_id': self.user_id,
            'biller_name': self.user.full_name if self.user else '',
            'total_amount': self.total_amount,
            'tax_amount': self.tax_amount,
            'discount_amount': self.discount_amount,
            'round_off': self.round_off,
            'net_amount': self.net_amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'item_count': len(self.items),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }

class BillItem(db.Model):
    __tablename__ = 'bill_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    returned_quantity = db.Column(db.Integer, nullable=False, default=0)
    tax_percent = db.Column(db.Float, nullable=False, default=0.0)
    tax_amount = db.Column(db.Float, nullable=False, default=0.0)
    total_price = db.Column(db.Float, nullable=False, default=0.0)

    product = db.relationship('Product', backref='bill_items', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'bill_id': self.bill_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'returned_quantity': self.returned_quantity or 0,
            'remaining_returnable_qty': max(0, self.quantity - (self.returned_quantity or 0)),
            'tax_percent': self.tax_percent,
            'tax_amount': self.tax_amount,
            'total_price': self.total_price
        }

class BillReturn(db.Model):
    __tablename__ = 'bill_returns'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    return_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    total_refund = db.Column(db.Float, nullable=False, default=0.0)
    refund_method = db.Column(db.String(30), nullable=False, default='Cash') # Cash, UPI, Card
    reason = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Completed') # Completed, Pending, Rejected
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    bill = db.relationship('Bill', backref='returns', lazy=True)
    customer = db.relationship('Customer', backref='returns', lazy=True)
    user = db.relationship('User', backref='returns', lazy=True)
    items = db.relationship('BillReturnItem', backref='bill_return', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'return_number': self.return_number,
            'bill_id': self.bill_id,
            'bill_number': self.bill.bill_number if self.bill else '',
            'customer_name': self.customer.name if self.customer else (self.bill.customer.name if self.bill and self.bill.customer else 'Walk-in Customer'),
            'customer_phone': self.customer.phone if self.customer else (self.bill.customer.phone if self.bill and self.bill.customer else ''),
            'total_refund': self.total_refund,
            'refund_method': self.refund_method,
            'reason': self.reason or 'Product Return',
            'status': self.status or 'Completed',
            'remarks': self.remarks or '',
            'processed_by': self.user.full_name if self.user else 'System Admin',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'item_count': len(self.items),
            'items': [
                {
                    'id': item.id,
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'sku': item.product.sku if item.product else 'N/A',
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'refund_amount': item.refund_amount,
                    'reason': item.reason or self.reason or 'Product Return',
                    'remarks': item.remarks or ''
                } for item in self.items
            ]
        }

class BillReturnItem(db.Model):
    __tablename__ = 'bill_return_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    return_id = db.Column(db.Integer, db.ForeignKey('bill_returns.id'), nullable=False)
    bill_item_id = db.Column(db.Integer, db.ForeignKey('bill_items.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    refund_amount = db.Column(db.Float, nullable=False, default=0.0)
    reason = db.Column(db.String(255), nullable=True)
    remarks = db.Column(db.Text, nullable=True)

    product = db.relationship('Product', lazy=True)

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
