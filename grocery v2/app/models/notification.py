from datetime import datetime
from app.database import db


class UserNotification(db.Model):
    """Persistent notification records — dismissals survive page refresh."""
    __tablename__ = 'user_notifications'

    id           = db.Column(db.Integer, primary_key=True)
    notif_type   = db.Column(db.String(20),  default='info', index=True)  # alert | activity
    icon         = db.Column(db.String(60),  default='fa-bell')
    title        = db.Column(db.String(200), nullable=False)
    message      = db.Column(db.String(500))
    link         = db.Column(db.String(255), default='#')
    created_by   = db.Column(db.String(100))      # user name who triggered it
    source_type  = db.Column(db.String(50),  index=True)  # low_stock|out_of_stock|expired|activity|bill|product|...
    source_id    = db.Column(db.Integer,     index=True)  # product_id, bill_id, activity_log_id
    is_dismissed = db.Column(db.Boolean,     default=False, index=True)
    created_at   = db.Column(db.DateTime,    default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id':           self.id,
            'notif_type':   self.notif_type,
            'icon':         self.icon,
            'title':        self.title,
            'message':      self.message,
            'link':         self.link,
            'created_by':   self.created_by or 'System',
            'source_type':  self.source_type,
            'is_dismissed': self.is_dismissed,
            'created_at':   self.created_at.strftime('%d %b, %I:%M %p') if self.created_at else ''
        }
