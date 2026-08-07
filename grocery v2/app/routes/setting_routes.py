import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.setting import SystemSetting
from app.database import db
from app.middleware.auth_middleware import admin_required

setting_bp = Blueprint('setting', __name__, url_prefix='/settings')

@setting_bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    if request.method == 'POST':
        # 1. Appearance
        dark_mode = 'on' if request.form.get('dark_mode') else 'off'
        theme_color = request.form.get('theme_color', 'blue')
        compact_sidebar = 'on' if request.form.get('compact_sidebar') else 'off'
        
        SystemSetting.set('DARK_MODE', dark_mode)
        SystemSetting.set('THEME_COLOR', theme_color)
        SystemSetting.set('COMPACT_SIDEBAR', compact_sidebar)

        # 2. Store Information
        store_name = request.form.get('store_name', '').strip()
        store_address = request.form.get('store_address', '').strip()
        gst_number = request.form.get('gst_number', '').strip()
        store_phone = request.form.get('store_phone', '').strip()
        
        if store_name:
            SystemSetting.set('STORE_NAME', store_name)
        if store_address:
            SystemSetting.set('STORE_ADDRESS', store_address)
        SystemSetting.set('GST_NUMBER', gst_number)
        if store_phone:
            SystemSetting.set('STORE_PHONE', store_phone)

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

        # 3. Billing
        invoice_prefix = request.form.get('invoice_prefix', 'INV').strip()
        enable_tax = 'on' if request.form.get('enable_tax') else 'off'
        enable_discount = 'on' if request.form.get('enable_discount') else 'off'
        print_logo = 'on' if request.form.get('print_logo_on_invoice') else 'off'
        
        SystemSetting.set('INVOICE_PREFIX', invoice_prefix or 'INV')
        SystemSetting.set('ENABLE_TAX', enable_tax)
        SystemSetting.set('ENABLE_DISCOUNT', enable_discount)
        SystemSetting.set('PRINT_LOGO_ON_INVOICE', print_logo)

        # 4. Inventory
        low_stock_thresh = request.form.get('low_stock_threshold', '10').strip()
        enable_expiry = 'on' if request.form.get('enable_expiry_tracking') else 'off'
        auto_sku = 'on' if request.form.get('auto_generate_sku') else 'off'

        SystemSetting.set('LOW_STOCK_THRESHOLD', low_stock_thresh or '10')
        SystemSetting.set('ENABLE_EXPIRY_TRACKING', enable_expiry)
        SystemSetting.set('AUTO_GENERATE_SKU', auto_sku)

        # 5. Security
        require_pwd_confirm = 'on' if request.form.get('require_pwd_confirm_delete') else 'off'
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

        SystemSetting.set('NOTIF_LOW_STOCK', notif_low_stock)
        SystemSetting.set('NOTIF_EXPIRY', notif_expiry)

        flash('System settings saved successfully!', 'success')
        return redirect(url_for('setting.index'))

    # GET Request: Collect Settings
    settings_data = {
        # Appearance
        'dark_mode': SystemSetting.get_bool('DARK_MODE', False),
        'theme_color': SystemSetting.get('THEME_COLOR', 'blue'),
        'compact_sidebar': SystemSetting.get_bool('COMPACT_SIDEBAR', False),

        # Store Info
        'store_name': SystemSetting.get('STORE_NAME', 'Smart Grocery Supermarket'),
        'store_logo': SystemSetting.get('STORE_LOGO', ''),
        'store_address': SystemSetting.get('STORE_ADDRESS', '123 Main High Street, Market City'),
        'gst_number': SystemSetting.get('GST_NUMBER', '27AAACG1234F1Z5'),
        'store_phone': SystemSetting.get('STORE_PHONE', '+91 98765 43210'),

        # Billing
        'invoice_prefix': SystemSetting.get('INVOICE_PREFIX', 'INV'),
        'enable_tax': SystemSetting.get_bool('ENABLE_TAX', True),
        'enable_discount': SystemSetting.get_bool('ENABLE_DISCOUNT', True),
        'print_logo_on_invoice': SystemSetting.get_bool('PRINT_LOGO_ON_INVOICE', True),

        # Inventory
        'low_stock_threshold': SystemSetting.get('LOW_STOCK_THRESHOLD', '10'),
        'enable_expiry_tracking': SystemSetting.get_bool('ENABLE_EXPIRY_TRACKING', True),
        'auto_generate_sku': SystemSetting.get_bool('AUTO_GENERATE_SKU', True),

        # Security
        'require_pwd_confirm_delete': SystemSetting.get_bool('REQUIRE_PWD_CONFIRM_DELETE', True),

        # Notifications
        'notif_low_stock': SystemSetting.get_bool('NOTIF_LOW_STOCK', True),
        'notif_expiry': SystemSetting.get_bool('NOTIF_EXPIRY', True),

        # About Metadata
        'app_version': 'v2.4.0',
        'developer_info': 'Smart Grocery Engineering Team',
        'db_status': 'Connected (SQLite Engine)'
    }

    return render_template('settings/index.html', settings=settings_data)

@setting_bp.route('/reset', methods=['POST'])
@login_required
@admin_required
def reset():
    SystemSetting.reset_defaults()
    flash('System settings reset to default values successfully.', 'warning')
    return redirect(url_for('setting.index'))
