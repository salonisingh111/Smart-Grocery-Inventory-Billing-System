import os
import json
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, Response
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.setting import SystemSetting
from app.models.product import Product
from app.models.user import User
from app.database import db
from app.middleware.auth_middleware import admin_required

setting_bp = Blueprint('setting', __name__, url_prefix='/settings')

@setting_bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    if request.method == 'POST':
        # 1. Store Information
        store_name = request.form.get('store_name', '').strip()
        store_phone = request.form.get('store_phone', '').strip()
        store_email = request.form.get('store_email', '').strip()
        gst_number = request.form.get('gst_number', '').strip()
        store_address = request.form.get('store_address', '').strip()

        if store_name:
            SystemSetting.set('STORE_NAME', store_name)
        if store_phone:
            SystemSetting.set('STORE_PHONE', store_phone)
        if store_email:
            SystemSetting.set('STORE_EMAIL', store_email)
        SystemSetting.set('GST_NUMBER', gst_number)
        if store_address:
            SystemSetting.set('STORE_ADDRESS', store_address)

        # Store Logo Upload
        logo_file = request.files.get('store_logo')
        if logo_file and logo_file.filename:
            filename = secure_filename(logo_file.filename)
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            save_path = os.path.join(upload_dir, filename)
            logo_file.save(save_path)
            rel_path = f'uploads/{filename}'
            SystemSetting.set('STORE_LOGO', rel_path)

        # 2. Regional & Business Settings
        currency_code = request.form.get('currency_code', 'INR').strip()
        currency_symbol = request.form.get('currency_symbol', '₹').strip()
        timezone = request.form.get('timezone', 'Asia/Kolkata').strip()
        date_format = request.form.get('date_format', 'DD/MM/YYYY').strip()
        tax_percentage = request.form.get('tax_percentage', '5.0').strip()

        SystemSetting.set('CURRENCY_CODE', currency_code or 'INR')
        SystemSetting.set('CURRENCY', currency_symbol or '₹')
        SystemSetting.set('TIMEZONE', timezone or 'Asia/Kolkata')
        SystemSetting.set('DATE_FORMAT', date_format or 'DD/MM/YYYY')
        SystemSetting.set('TAX_PERCENTAGE', tax_percentage or '5.0')

        # 3. Billing & Invoice
        invoice_prefix = request.form.get('invoice_prefix', 'INV').strip()
        next_invoice_number = request.form.get('next_invoice_number', '1001').strip()
        enable_tax = 'on' if request.form.get('enable_tax') else 'off'
        enable_discount = 'on' if request.form.get('enable_discount') else 'off'
        print_logo = 'on' if request.form.get('print_logo_on_invoice') else 'off'
        invoice_footer_msg = request.form.get('invoice_footer_msg', '').strip()
        invoice_format = request.form.get('invoice_format', '80mm Thermal Receipt').strip()
        default_payment_method = request.form.get('default_payment_method', 'Cash').strip()

        SystemSetting.set('INVOICE_PREFIX', invoice_prefix or 'INV')
        SystemSetting.set('NEXT_INVOICE_NUMBER', next_invoice_number or '1001')
        SystemSetting.set('ENABLE_TAX', enable_tax)
        SystemSetting.set('ENABLE_DISCOUNT', enable_discount)
        SystemSetting.set('PRINT_LOGO_ON_INVOICE', print_logo)
        SystemSetting.set('INVOICE_FOOTER_MSG', invoice_footer_msg)
        SystemSetting.set('INVOICE_FORMAT', invoice_format)
        SystemSetting.set('DEFAULT_PAYMENT_METHOD', default_payment_method)

        # 4. Inventory Controls
        low_stock_thresh = request.form.get('low_stock_threshold', '10').strip()
        enable_expiry = 'on' if request.form.get('enable_expiry_tracking') else 'off'
        auto_sku = 'on' if request.form.get('auto_generate_sku') else 'off'
        allow_negative_stock = 'on' if request.form.get('allow_negative_stock') else 'off'
        default_product_unit = request.form.get('default_product_unit', 'pcs').strip()

        SystemSetting.set('LOW_STOCK_THRESHOLD', low_stock_thresh or '10')
        SystemSetting.set('ENABLE_EXPIRY_TRACKING', enable_expiry)
        SystemSetting.set('AUTO_GENERATE_SKU', auto_sku)
        SystemSetting.set('ALLOW_NEGATIVE_STOCK', allow_negative_stock)
        SystemSetting.set('DEFAULT_PRODUCT_UNIT', default_product_unit or 'pcs')

        # 5. Security & Passwords
        session_timeout = request.form.get('session_timeout_mins', '30').strip()
        require_pwd_confirm = 'on' if request.form.get('require_pwd_confirm_delete') else 'off'
        
        SystemSetting.set('SESSION_TIMEOUT_MINS', session_timeout or '30')
        SystemSetting.set('REQUIRE_PWD_CONFIRM_DELETE', require_pwd_confirm)

        current_pwd = request.form.get('current_password', '').strip()
        new_pwd = request.form.get('new_password', '').strip()
        confirm_pwd = request.form.get('confirm_password', '').strip()

        if new_pwd:
            if not current_user.check_password(current_pwd):
                flash('Security Error: Current password was incorrect. Password not changed.', 'danger')
            elif new_pwd != confirm_pwd:
                flash('Security Error: New password confirmation does not match.', 'danger')
            else:
                current_user.set_password(new_pwd)
                db.session.commit()
                flash('Account security password updated successfully.', 'success')

        # 6. Notifications
        notif_low_stock = 'on' if request.form.get('notif_low_stock') else 'off'
        notif_expiry = 'on' if request.form.get('notif_expiry') else 'off'
        notif_sales = 'on' if request.form.get('notif_sales') else 'off'
        notif_system = 'on' if request.form.get('notif_system') else 'off'

        SystemSetting.set('NOTIF_LOW_STOCK', notif_low_stock)
        SystemSetting.set('NOTIF_EXPIRY', notif_expiry)
        SystemSetting.set('NOTIF_SALES', notif_sales)
        SystemSetting.set('NOTIF_SYSTEM', notif_system)

        flash('System settings saved successfully!', 'success')
        return redirect(url_for('setting.index'))

    # GET Request: Dynamic Database Detection & Data Collection
    raw_engine = db.engine.name.lower()
    if 'mysql' in raw_engine:
        db_engine_name = 'MySQL'
    elif 'sqlite' in raw_engine:
        db_engine_name = 'SQLite'
    else:
        db_engine_name = raw_engine.upper()

    try:
        db.session.execute(db.text('SELECT 1'))
        db_conn_status = 'Connected'
    except Exception:
        db_conn_status = 'Disconnected'

    settings_data = {
        # Store Information
        'store_name': SystemSetting.get('STORE_NAME', 'Smart Grocery Supermarket'),
        'store_phone': SystemSetting.get('STORE_PHONE', '+91 98765 43210'),
        'store_email': SystemSetting.get('STORE_EMAIL', 'support@smartgrocery.com'),
        'gst_number': SystemSetting.get('GST_NUMBER', '27AAACG1234F1Z5'),
        'store_address': SystemSetting.get('STORE_ADDRESS', '123 Main High Street, Market City'),
        'store_logo': SystemSetting.get('STORE_LOGO', ''),

        # Regional & Business Settings
        'currency_code': SystemSetting.get('CURRENCY_CODE', 'INR'),
        'currency_symbol': SystemSetting.get('CURRENCY', '₹'),
        'timezone': SystemSetting.get('TIMEZONE', 'Asia/Kolkata'),
        'date_format': SystemSetting.get('DATE_FORMAT', 'DD/MM/YYYY'),
        'tax_percentage': SystemSetting.get('TAX_PERCENTAGE', '5.0'),

        # Billing & Invoice
        'invoice_prefix': SystemSetting.get('INVOICE_PREFIX', 'INV'),
        'next_invoice_number': SystemSetting.get('NEXT_INVOICE_NUMBER', '1001'),
        'enable_tax': SystemSetting.get_bool('ENABLE_TAX', True),
        'enable_discount': SystemSetting.get_bool('ENABLE_DISCOUNT', True),
        'print_logo_on_invoice': SystemSetting.get_bool('PRINT_LOGO_ON_INVOICE', True),
        'invoice_footer_msg': SystemSetting.get('INVOICE_FOOTER_MSG', 'Thank you for shopping with Smart Grocery Supermarket!'),
        'invoice_format': SystemSetting.get('INVOICE_FORMAT', '80mm Thermal Receipt'),
        'default_payment_method': SystemSetting.get('DEFAULT_PAYMENT_METHOD', 'Cash'),

        # Inventory Controls
        'low_stock_threshold': SystemSetting.get('LOW_STOCK_THRESHOLD', '10'),
        'enable_expiry_tracking': SystemSetting.get_bool('ENABLE_EXPIRY_TRACKING', True),
        'auto_generate_sku': SystemSetting.get_bool('AUTO_GENERATE_SKU', True),
        'allow_negative_stock': SystemSetting.get_bool('ALLOW_NEGATIVE_STOCK', False),
        'default_product_unit': SystemSetting.get('DEFAULT_PRODUCT_UNIT', 'pcs'),

        # Security
        'session_timeout_mins': SystemSetting.get('SESSION_TIMEOUT_MINS', '30'),
        'require_pwd_confirm_delete': SystemSetting.get_bool('REQUIRE_PWD_CONFIRM_DELETE', True),

        # Notifications
        'notif_low_stock': SystemSetting.get_bool('NOTIF_LOW_STOCK', True),
        'notif_expiry': SystemSetting.get_bool('NOTIF_EXPIRY', True),
        'notif_sales': SystemSetting.get_bool('NOTIF_SALES', True),
        'notif_system': SystemSetting.get_bool('NOTIF_SYSTEM', True),

        # Data & Backup Metadata
        'last_backup': SystemSetting.get('LAST_BACKUP_TIME', 'Ready (No Backup Yet)'),

        # About Metadata
        'app_version': 'v2.4.0',
        'developer_info': 'Smart Grocery Engineering Team',
        'db_engine': db_engine_name,
        'db_status': db_conn_status
    }

    return render_template('settings/index.html', settings=settings_data)

@setting_bp.route('/export-backup', methods=['GET'])
@login_required
@admin_required
def export_backup():
    all_settings = SystemSetting.query.all()
    backup_data = {
        'system': 'Smart Grocery Inventory & Billing System',
        'exported_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'exported_by': current_user.username,
        'total_products': Product.query.count(),
        'total_users': User.query.count(),
        'settings': {s.setting_key: s.setting_value for s in all_settings}
    }

    # Log timestamp of backup
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    SystemSetting.set('LAST_BACKUP_TIME', now_str)

    json_str = json.dumps(backup_data, indent=2)
    filename = f"smart_grocery_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    return Response(
        json_str,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

@setting_bp.route('/reset', methods=['POST'])
@login_required
@admin_required
def reset():
    # Restore standard defaults
    defaults = {
        'STORE_NAME': 'Smart Grocery Supermarket',
        'STORE_PHONE': '+91 98765 43210',
        'STORE_EMAIL': 'support@smartgrocery.com',
        'GST_NUMBER': '27AAACG1234F1Z5',
        'STORE_ADDRESS': '123 Main High Street, Market City',
        'CURRENCY_CODE': 'INR',
        'CURRENCY': '₹',
        'TIMEZONE': 'Asia/Kolkata',
        'DATE_FORMAT': 'DD/MM/YYYY',
        'TAX_PERCENTAGE': '5.0',
        'INVOICE_PREFIX': 'INV',
        'NEXT_INVOICE_NUMBER': '1001',
        'ENABLE_TAX': 'on',
        'ENABLE_DISCOUNT': 'on',
        'PRINT_LOGO_ON_INVOICE': 'on',
        'INVOICE_FOOTER_MSG': 'Thank you for shopping with Smart Grocery Supermarket!',
        'INVOICE_FORMAT': '80mm Thermal Receipt',
        'DEFAULT_PAYMENT_METHOD': 'Cash',
        'LOW_STOCK_THRESHOLD': '10',
        'ENABLE_EXPIRY_TRACKING': 'on',
        'AUTO_GENERATE_SKU': 'on',
        'ALLOW_NEGATIVE_STOCK': 'off',
        'DEFAULT_PRODUCT_UNIT': 'pcs',
        'SESSION_TIMEOUT_MINS': '30',
        'REQUIRE_PWD_CONFIRM_DELETE': 'on',
        'NOTIF_LOW_STOCK': 'on',
        'NOTIF_EXPIRY': 'on',
        'NOTIF_SALES': 'on',
        'NOTIF_SYSTEM': 'on'
    }
    for k, v in defaults.items():
        SystemSetting.set(k, v)

    flash('System settings reset to default values successfully.', 'warning')
    return redirect(url_for('setting.index'))
