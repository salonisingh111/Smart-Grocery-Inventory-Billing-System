from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models.activity_log import ActivityLog
from app.middleware.auth_middleware import admin_required

activity_bp = Blueprint('activity', __name__, url_prefix='/activity-logs')

@activity_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    search = request.args.get('search', '').strip()
    action_filter = request.args.get('action', '').strip()
    page = request.args.get('page', 1, type=int)

    query = ActivityLog.query

    if search:
        query = query.filter(
            (ActivityLog.user_name.ilike(f'%{search}%')) |
            (ActivityLog.action.ilike(f'%{search}%')) |
            (ActivityLog.details.ilike(f'%{search}%')) |
            (ActivityLog.ip_address.ilike(f'%{search}%'))
        )

    if action_filter:
        query = query.filter(ActivityLog.action == action_filter)

    pagination = query.order_by(ActivityLog.id.desc()).paginate(page=page, per_page=20, error_out=False)
    logs = pagination.items

    actions_list = ActivityLog.query.with_entities(ActivityLog.action).distinct().all()
    actions = [a[0] for a in actions_list if a[0]]

    return render_template(
        'activity/index.html',
        logs=logs,
        pagination=pagination,
        search=search,
        action_filter=action_filter,
        actions=actions
    )
