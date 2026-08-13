"""
Notification utility helpers.
All notification creation and stock-alert syncing lives here
so routes stay thin.
"""
from app.database import db
from app.models.notification import UserNotification

# ─── Icon / type maps ──────────────────────────────────────────────────────────
ACTION_ICON_MAP = {
    'New Bill':             ('fa-receipt',            'activity'),
    'Cancel Bill':          ('fa-ban',                'activity'),
    'Return Items':         ('fa-rotate-left',        'activity'),
    'Add Product':          ('fa-plus-circle',        'activity'),
    'Edit Product':         ('fa-pen',                'activity'),
    'Delete Product':       ('fa-trash',              'activity'),
    'Export Products':      ('fa-file-csv',           'activity'),
    'Export Report':        ('fa-file-export',        'activity'),
    'Export Sales Report':  ('fa-file-excel',         'activity'),
    'Export System Backup': ('fa-file-zipper',        'activity'),
    'Add Category':         ('fa-tag',                'activity'),
    'Edit Category':        ('fa-tag',                'activity'),
    'Delete Category':      ('fa-tag',                'activity'),
    'Add Supplier':         ('fa-truck',              'activity'),
    'Edit Supplier':        ('fa-truck',              'activity'),
    'Delete Supplier':      ('fa-truck',              'activity'),
    'Register Customer':    ('fa-user-plus',          'activity'),
    'Edit Customer':        ('fa-user-pen',           'activity'),
    'Delete Customer':      ('fa-user-minus',         'activity'),
    'Stock Adjustment':     ('fa-boxes-stacked',      'activity'),
    'Create User':          ('fa-user-plus',          'activity'),
    'Update User':          ('fa-user-pen',           'activity'),
    'Delete User':          ('fa-user-minus',         'activity'),
    'Toggle User Status':   ('fa-user-shield',        'activity'),
    'User Login':           ('fa-right-to-bracket',   'activity'),
    'User Logout':          ('fa-right-from-bracket', 'activity'),
    'Update Profile':       ('fa-id-card',            'activity'),
    'Password Change':      ('fa-key',                'activity'),
    'Settings Updated':     ('fa-sliders',            'activity'),
    'Reset Settings':       ('fa-rotate-left',        'activity'),
    'Failed Login Attempt': ('fa-lock',               'activity'),
}


def create_activity_notification(action: str, details: str,
                                 source_id: int = None,
                                 created_by: str = None,
                                 link: str = '/activity-logs/'):
    """
    Persist an activity notification row.
    Prevent duplicate creation if source_id is already present.
    """
    try:
        if source_id:
            existing = UserNotification.query.filter_by(source_type='activity', source_id=source_id).first()
            if existing:
                return

        icon, ntype = ACTION_ICON_MAP.get(action, ('fa-circle-dot', 'activity'))
        notif = UserNotification(
            notif_type='activity',
            icon=icon,
            title=action,
            message=details,
            link=link,
            source_type='activity',
            source_id=source_id,
            created_by=created_by,
        )
        db.session.add(notif)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'[notifications] create_activity_notification error: {e}')


def sync_stock_alerts_for_product(product_id: int):
    """
    Delete-and-recreate stock alert notifications for ONE product.
    Call this whenever a product's quantity changes (save, stock-adjust, bill).
    Old dismissed alerts are cleared so the user sees fresh ones when stock changes.
    """
    try:
        from app.models.product import Product

        p = Product.query.get(product_id)
        if not p:
            return

        stock_types = ('low_stock', 'out_of_stock', 'expired')
        # Delete ALL old stock alerts for this product (incl. dismissed)
        UserNotification.query.filter(
            UserNotification.source_type.in_(stock_types),
            UserNotification.source_id == product_id
        ).delete(synchronize_session=False)

        if p.status == 'Active':
            if p.quantity == 0:
                db.session.add(UserNotification(
                    notif_type='alert',
                    icon='fa-circle-xmark',
                    title='Out of Stock',
                    message=f'{p.name} is completely out of stock',
                    link='/products/?stock_status=out',
                    source_type='out_of_stock',
                    source_id=p.id,
                ))
            elif p.is_low_stock():
                db.session.add(UserNotification(
                    notif_type='alert',
                    icon='fa-triangle-exclamation',
                    title='Low Stock Alert',
                    message=f'{p.name} — only {p.quantity} {p.unit} left',
                    link='/products/?stock_status=low',
                    source_type='low_stock',
                    source_id=p.id,
                ))

            if p.is_expired():
                db.session.add(UserNotification(
                    notif_type='alert',
                    icon='fa-skull-crossbones',
                    title='Expired Product',
                    message=f'{p.name} has expired and must be removed',
                    link='/products/?stock_status=expired',
                    source_type='expired',
                    source_id=p.id,
                ))

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'[notifications] sync_stock_alerts_for_product error: {e}')


def initial_sync_all_stock_alerts():
    """
    Incremental resync of ALL stock alerts.
    Called once on server startup. Preserves is_dismissed status of existing alerts!
    """
    try:
        from app.models.product import Product

        stock_types = ('low_stock', 'out_of_stock', 'expired')
        # Load all existing stock alerts from DB
        existing_alerts = UserNotification.query.filter(
            UserNotification.source_type.in_(stock_types)
        ).all()

        # Map by (source_type, source_id) -> UserNotification object
        alert_map = {(n.source_type, n.source_id): n for n in existing_alerts}
        required_alerts = []

        active_products = Product.query.filter_by(status='Active').all()
        for p in active_products:
            # Out of stock alert
            if p.quantity == 0:
                required_alerts.append(('out_of_stock', p.id, {
                    'notif_type': 'alert',
                    'icon': 'fa-circle-xmark',
                    'title': 'Out of Stock',
                    'message': f'{p.name} is completely out of stock',
                    'link': '/products/?stock_status=out',
                    'source_type': 'out_of_stock',
                    'source_id': p.id,
                }))
            # Low stock alert
            elif p.is_low_stock():
                required_alerts.append(('low_stock', p.id, {
                    'notif_type': 'alert',
                    'icon': 'fa-triangle-exclamation',
                    'title': 'Low Stock Alert',
                    'message': f'{p.name} — only {p.quantity} {p.unit} left',
                    'link': '/products/?stock_status=low',
                    'source_type': 'low_stock',
                    'source_id': p.id,
                }))

            # Expired alert
            if p.is_expired():
                required_alerts.append(('expired', p.id, {
                    'notif_type': 'alert',
                    'icon': 'fa-skull-crossbones',
                    'title': 'Expired Product',
                    'message': f'{p.name} has expired and must be removed',
                    'link': '/products/?stock_status=expired',
                    'source_type': 'expired',
                    'source_id': p.id,
                }))

        # Track keys we need to keep
        keep_keys = set()

        # Process required alerts
        for stype, sid, data in required_alerts:
            key = (stype, sid)
            keep_keys.add(key)
            if key not in alert_map:
                # Insert new alert
                db.session.add(UserNotification(**data))

        # Delete any alerts in DB that are no longer active/required
        for key, notif in alert_map.items():
            if key not in keep_keys:
                db.session.delete(notif)

        db.session.commit()
        print('[notifications] initial_sync_all_stock_alerts complete (incremental).')
    except Exception as e:
        db.session.rollback()
        print(f'[notifications] initial_sync_all_stock_alerts error: {e}')
