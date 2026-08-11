from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models.activity_log import ActivityLog
from app.models.user import User
from app.middleware.auth_middleware import admin_required

activity_bp = Blueprint('activity', __name__, url_prefix='/activity-logs')

EXCLUDED_BUSINESS_ACTIONS = [
    'New Bill', 'Add Product', 'Edit Product', 'Delete Product',
    'Stock Adjustment', 'Add Supplier', 'Edit Supplier', 'Delete Supplier',
    'Register Customer', 'Edit Customer', 'Delete Customer',
    'Add Category', 'Edit Category', 'Delete Category'
]

@activity_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    search = request.args.get('search', '').strip()
    action_filter = request.args.get('action', '').strip()
    user_id_filter = request.args.get('user_id', type=int)
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    page = request.args.get('page', 1, type=int)

    # Base query: focus on User & Security activities
    query = ActivityLog.query.filter(~ActivityLog.action.in_(EXCLUDED_BUSINESS_ACTIONS))

    if search:
        query = query.filter(
            (ActivityLog.user_name.ilike(f'%{search}%')) |
            (ActivityLog.action.ilike(f'%{search}%')) |
            (ActivityLog.details.ilike(f'%{search}%')) |
            (ActivityLog.ip_address.ilike(f'%{search}%'))
        )

    if action_filter:
        query = query.filter(ActivityLog.action == action_filter)

    if user_id_filter:
        query = query.filter(ActivityLog.user_id == user_id_filter)

    if start_date:
        try:
            s_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(ActivityLog.created_at >= s_dt)
        except ValueError:
            pass

    if end_date:
        try:
            e_dt = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
            query = query.filter(ActivityLog.created_at <= e_dt)
        except ValueError:
            pass

    logs = query.order_by(ActivityLog.id.desc()).all()

    # Action dropdown options from user/security logs
    actions_list = ActivityLog.query.filter(~ActivityLog.action.in_(EXCLUDED_BUSINESS_ACTIONS)).with_entities(ActivityLog.action).distinct().all()
    actions = sorted([a[0] for a in actions_list if a[0]])

    all_users = User.query.order_by(User.full_name).all()

    return render_template(
        'activity/index.html',
        logs=logs,
        search=search,
        action_filter=action_filter,
        user_id_filter=user_id_filter,
        start_date=start_date,
        end_date=end_date,
        actions=actions,
        all_users=all_users
    )
