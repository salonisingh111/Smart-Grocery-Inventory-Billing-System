from flask import Flask, render_template
from config import Config
from app.database import db
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register models user loader
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Context Processors
    @app.context_processor
    def inject_global_settings():
        from app.models.setting import SystemSetting
        from flask_login import current_user

        base_ctx = {
            'dark_mode': SystemSetting.get_bool('DARK_MODE', False),
            'theme_color': SystemSetting.get('THEME_COLOR', 'blue'),
            'compact_sidebar': SystemSetting.get_bool('COMPACT_SIDEBAR', False),
            'store_name': SystemSetting.get('STORE_NAME', 'Smart Grocery System'),
            'store_logo': SystemSetting.get('STORE_LOGO', ''),
            'store_address': SystemSetting.get('STORE_ADDRESS', ''),
            'gst_number': SystemSetting.get('GST_NUMBER', ''),
            'store_phone': SystemSetting.get('STORE_PHONE', ''),
            'store_email': SystemSetting.get('STORE_EMAIL', ''),
            'invoice_prefix': SystemSetting.get('INVOICE_PREFIX', 'INV'),
            'enable_tax': SystemSetting.get_bool('ENABLE_TAX', True),
            'enable_discount': SystemSetting.get_bool('ENABLE_DISCOUNT', True),
            'print_logo_on_invoice': SystemSetting.get_bool('PRINT_LOGO_ON_INVOICE', True),
            'low_stock_threshold': int(SystemSetting.get('LOW_STOCK_THRESHOLD', '10') or '10'),
            'enable_expiry_tracking': SystemSetting.get_bool('ENABLE_EXPIRY_TRACKING', True),
            'auto_generate_sku': SystemSetting.get_bool('AUTO_GENERATE_SKU', True),
            'require_pwd_confirm_delete': SystemSetting.get_bool('REQUIRE_PWD_CONFIRM_DELETE', True),
            'notif_low_stock': SystemSetting.get_bool('NOTIF_LOW_STOCK', True),
            'notif_expiry': SystemSetting.get_bool('NOTIF_EXPIRY', True),
            'currency_symbol': SystemSetting.get('CURRENCY', '₹'),
            'nav_notifications': [],
            'nav_notif_count': 0,
            'nav_activity': []
        }

        # ── Read navbar notifications from DB (fast, single query) ──────────
        try:
            if current_user.is_authenticated:
                from app.models.notification import UserNotification

                all_notifs = (
                    UserNotification.query
                    .filter_by(is_dismissed=False)
                    .order_by(UserNotification.created_at.desc())
                    .all()
                )

                raw_alerts   = [n for n in all_notifs if n.notif_type == 'alert']
                raw_activity = [n for n in all_notifs if n.notif_type == 'activity']

                # Alerts tab
                nav_notifications = []
                TYPE_MAP = {'low_stock': 'warning', 'out_of_stock': 'danger', 'expired': 'danger'}
                for n in raw_alerts:
                    nav_notifications.append({
                        'id':      n.id,
                        'type':    TYPE_MAP.get(n.source_type, 'warning'),
                        'icon':    n.icon,
                        'title':   n.title,
                        'message': n.message,
                        'link':    n.link,
                    })

                # Activity tab
                nav_activity = []
                for n in raw_activity[:15]:
                    nav_activity.append({
                        'id':      n.id,
                        'icon':    n.icon,
                        'type':    'info',
                        'action':  n.title,
                        'details': n.message or '',
                        'user':    n.created_by or 'System',
                        'time':    n.created_at.strftime('%d %b, %I:%M %p') if n.created_at else '',
                        'link':    n.link or '/activity-logs/',
                    })

                base_ctx['nav_notifications'] = nav_notifications
                base_ctx['nav_activity']      = nav_activity
                base_ctx['nav_notif_count']   = len(raw_alerts) + len(raw_activity)
        except Exception:
            pass

        return base_ctx

    # Register Blueprints
    from app.routes.notification_routes import notif_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.product_routes import product_bp
    from app.routes.category_routes import category_bp
    from app.routes.supplier_routes import supplier_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.inventory_routes import inventory_bp
    from app.routes.billing_routes import billing_bp
    from app.routes.report_routes import report_bp
    from app.routes.setting_routes import setting_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(notif_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(setting_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(user_bp)

    # Custom Error Handlers (Never expose Flask tracebacks or DB exceptions)
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    return app
