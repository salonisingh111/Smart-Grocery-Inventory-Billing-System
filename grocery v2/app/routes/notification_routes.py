from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.database import db
from app.models.notification import UserNotification

notif_bp = Blueprint('notif', __name__, url_prefix='/api/notifications')


@notif_bp.route('/dismiss/<int:notif_id>', methods=['POST'])
@login_required
def dismiss(notif_id):
    """Mark a single notification as dismissed (persisted in DB)."""
    notif = UserNotification.query.get(notif_id)
    if notif:
        notif.is_dismissed = True
        db.session.commit()
    return jsonify({'success': True})


@notif_bp.route('/dismiss-all', methods=['POST'])
@login_required
def dismiss_all():
    """Mark all non-dismissed notifications of a given type as dismissed."""
    data      = request.get_json() or {}
    tab_type  = data.get('type')   # 'alert' | 'activity' | None → all

    query = UserNotification.query.filter_by(is_dismissed=False)
    if tab_type in ('alert', 'activity'):
        query = query.filter_by(notif_type=tab_type)

    query.update({'is_dismissed': True}, synchronize_session=False)
    db.session.commit()
    return jsonify({'success': True})


@notif_bp.route('/count', methods=['GET'])
@login_required
def count():
    """Return current unread notification count (for badge polling)."""
    total = UserNotification.query.filter_by(is_dismissed=False).count()
    return jsonify({'count': total})
