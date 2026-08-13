from flask import request
from flask_login import current_user
from app.database import db
from app.models.activity_log import ActivityLog

def log_activity(action: str, details: str = None, user_id: int = None, user_name: str = None):
    """
    Utility function to record a system activity log into the database
    and automatically create a real-time persistent user notification.
    """
    try:
        ip = None
        if request:
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ip and ',' in ip:
                ip = ip.split(',')[0].strip()

        target_user_id = user_id
        target_user_name = user_name

        if not target_user_id and current_user and current_user.is_authenticated:
            target_user_id = current_user.id
            target_user_name = current_user.full_name

        log_entry = ActivityLog(
            user_id=target_user_id,
            user_name=target_user_name or 'System',
            action=action,
            details=details,
            ip_address=ip
        )
        db.session.add(log_entry)
        db.session.commit()

        # Automatically sync notification for this activity
        try:
            from app.utils.notifications import create_activity_notification
            create_activity_notification(
                action=action,
                details=details or '',
                source_id=log_entry.id,
                created_by=target_user_name or 'System',
                link='/activity-logs/'
            )
        except Exception as notif_err:
            print(f"Failed to create notification for activity '{action}': {notif_err}")

    except Exception as e:
        db.session.rollback()
        print(f"Failed to log activity '{action}': {e}")
