from datetime import datetime
from app.database import db

DEFAULT_SETTINGS = {
    'DARK_MODE': 'off',
    'THEME_COLOR': 'blue',
    'COMPACT_SIDEBAR': 'off',
    'STORE_NAME': 'Smart Billing',
    'STORE_LOGO': '',
    'STORE_ADDRESS': '123 Main High Street, Market City',
    'GST_NUMBER': '27AAACG1234F1Z5',
    'STORE_PHONE': '+91 98765 43210',
    'STORE_EMAIL': 'support@smartgrocery.com',
    'INVOICE_PREFIX': 'INV',
    'ENABLE_TAX': 'on',
    'ENABLE_DISCOUNT': 'on',
    'PRINT_LOGO_ON_INVOICE': 'on',
    'LOW_STOCK_THRESHOLD': '10',
    'ENABLE_EXPIRY_TRACKING': 'on',
    'AUTO_GENERATE_SKU': 'on',
    'REQUIRE_PWD_CONFIRM_DELETE': 'on',
    'NOTIF_LOW_STOCK': 'on',
    'NOTIF_EXPIRY': 'on',
    'CURRENCY': '₹',
    'TAX_PERCENTAGE': '5.0'
}

class SystemSetting(db.Model):
    __tablename__ = 'system_settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    setting_key = db.Column(db.String(50), unique=True, nullable=False, index=True)
    setting_value = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get(cls, key: str, default: str = None) -> str:
        fallback = default if default is not None else DEFAULT_SETTINGS.get(key, '')
        setting = cls.query.filter_by(setting_key=key).first()
        return setting.setting_value if setting and setting.setting_value is not None else fallback

    @classmethod
    def get_bool(cls, key: str, default: bool = False) -> bool:
        val = cls.get(key, 'on' if default else 'off')
        return val.lower() in ['on', 'true', '1', 'yes']

    @classmethod
    def set(cls, key: str, value: str, description: str = None):
        setting = cls.query.filter_by(setting_key=key).first()
        if not setting:
            setting = cls(setting_key=key, setting_value=str(value), description=description)
            db.session.add(setting)
        else:
            setting.setting_value = str(value)
            if description:
                setting.description = description
        db.session.commit()

    @classmethod
    def reset_defaults(cls):
        for key, val in DEFAULT_SETTINGS.items():
            setting = cls.query.filter_by(setting_key=key).first()
            if not setting:
                setting = cls(setting_key=key, setting_value=val)
                db.session.add(setting)
            else:
                setting.setting_value = val
        db.session.commit()
