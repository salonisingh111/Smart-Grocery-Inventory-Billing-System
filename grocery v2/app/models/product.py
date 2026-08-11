from datetime import datetime, timedelta
from app.database import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    barcode = db.Column(db.String(50), unique=True, nullable=True, index=True)
    qr_code = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    
    purchase_price = db.Column(db.Float, nullable=False, default=0.0)
    selling_price = db.Column(db.Float, nullable=False, default=0.0)
    tax_percent = db.Column(db.Float, nullable=False, default=0.0)
    discount_percent = db.Column(db.Float, nullable=False, default=0.0)
    
    quantity = db.Column(db.Integer, nullable=False, default=0)
    min_stock = db.Column(db.Integer, nullable=False, default=10)
    max_stock = db.Column(db.Integer, nullable=False, default=500)
    
    expiry_date = db.Column(db.Date, nullable=True)
    mfd_date = db.Column(db.Date, nullable=True)
    unit = db.Column(db.String(20), nullable=False, default='pcs')  # pcs, kg, g, l, ml, box, pkt
    image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Active')  # Active, Inactive
    notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    inventory_logs = db.relationship('InventoryHistory', backref='product', lazy=True, cascade="all, delete-orphan")

    def is_low_stock(self) -> bool:
        from app.models.setting import SystemSetting
        thresh = int(SystemSetting.get('LOW_STOCK_THRESHOLD', '10') or '10')
        effective_limit = self.min_stock if self.min_stock > 0 else thresh
        return 0 < self.quantity <= effective_limit

    def is_out_of_stock(self) -> bool:
        return self.quantity <= 0

    def is_expired(self) -> bool:
        if not self.expiry_date:
            return False
        return self.expiry_date < datetime.utcnow().date()

    def is_near_expiry(self) -> bool:
        if not self.expiry_date:
            return False
        from app.models.setting import SystemSetting
        warning_days = int(SystemSetting.get('EXPIRY_WARNING_DAYS', '30') or '30')
        today = datetime.utcnow().date()
        return today <= self.expiry_date <= (today + timedelta(days=warning_days))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'barcode': self.barcode or '',
            'qr_code': self.qr_code or '',
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else '',
            'brand': self.brand or '',
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if self.supplier else '',
            'purchase_price': self.purchase_price,
            'selling_price': self.selling_price,
            'tax_percent': self.tax_percent,
            'discount_percent': self.discount_percent,
            'quantity': self.quantity,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else '',
            'mfd_date': self.mfd_date.strftime('%Y-%m-%d') if self.mfd_date else '',
            'unit': self.unit,
            'image': self.image or '',
            'status': self.status,
            'is_low_stock': self.is_low_stock(),
            'is_out_of_stock': self.is_out_of_stock(),
            'is_expired': self.is_expired(),
            'notes': self.notes or ''
        }
