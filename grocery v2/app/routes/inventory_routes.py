from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.inventory import InventoryHistory
from app.models.user import User
from app.services.inventory_service import InventoryService
from app.services.auth_service import verify_sensitive_password
from app.validators.forms import StockAdjustmentForm
from app.utils.logger import log_activity
from app.utils.notifications import create_activity_notification, sync_stock_alerts_for_product

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = StockAdjustmentForm()
    active_products = Product.query.filter_by(status='Active').order_by(Product.name).all()
    all_users = User.query.order_by(User.full_name).all()

    if request.method == 'POST':
        confirm_pwd = request.form.get('confirm_password', '')
        if confirm_pwd and not verify_sensitive_password(confirm_pwd):
            flash('Action Denied: Incorrect password confirmation.', 'danger')
            return redirect(url_for('inventory.index'))

        product_id = request.form.get('product_id', type=int)
        change_type = request.form.get('change_type', 'Stock Out', type=str)
        qty_input = request.form.get('quantity_changed', type=int) or 0
        reason = request.form.get('reason', '', type=str)
        remarks = request.form.get('remarks', '', type=str)

        qty_change = -abs(qty_input) if change_type == 'Stock Out' else abs(qty_input)

        success, msg = InventoryService.adjust_stock(
            product_id=product_id,
            quantity_change=qty_change,
            change_type=change_type,
            reason=reason,
            user_id=current_user.id,
            remarks=remarks
        )

        if success:
            product = Product.query.get(product_id)
            pname = product.name if product else f'ID#{product_id}'
            log_activity('Stock Audit Adjustment', f'{change_type}: {abs(qty_input)} units of "{pname}" — Reason: {reason or "No reason given"}')
            create_activity_notification('Stock Audit Adjustment', f'{change_type}: {abs(qty_input)} units of "{pname}"', created_by=current_user.full_name)
            sync_stock_alerts_for_product(product_id)
            flash(msg, 'success')
        else:
            flash(msg, 'danger')

        return redirect(url_for('inventory.index'))

    search = request.args.get('search', '', type=str).strip()
    change_type_filter = request.args.get('change_type', '', type=str).strip()
    reason_filter = request.args.get('reason', '', type=str).strip()
    user_id_filter = request.args.get('user_id', type=int)
    start_date = request.args.get('start_date', '', type=str).strip()
    end_date = request.args.get('end_date', '', type=str).strip()
    page = request.args.get('page', 1, type=int)

    query = InventoryHistory.query.join(Product)

    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.sku.ilike(f"%{search}%")) |
            (InventoryHistory.reason.ilike(f"%{search}%")) |
            (InventoryHistory.reference_code.ilike(f"%{search}%"))
        )

    if change_type_filter:
        query = query.filter(InventoryHistory.change_type == change_type_filter)

    if reason_filter:
        query = query.filter(InventoryHistory.reason == reason_filter)

    if user_id_filter:
        query = query.filter(InventoryHistory.performed_by_user_id == user_id_filter)

    if start_date:
        try:
            s_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(InventoryHistory.created_at >= s_dt)
        except ValueError:
            pass

    if end_date:
        try:
            e_dt = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
            query = query.filter(InventoryHistory.created_at <= e_dt)
        except ValueError:
            pass

    logs = query.order_by(InventoryHistory.created_at.desc()).all()

    reasons_list = InventoryHistory.query.with_entities(InventoryHistory.reason).distinct().all()
    reasons = sorted([r[0] for r in reasons_list if r[0]])

    return render_template(
        'inventory/index.html',
        logs=logs,
        products=active_products,
        all_users=all_users,
        reasons=reasons,
        form=form,
        search=search,
        change_type_filter=change_type_filter,
        reason_filter=reason_filter,
        user_id_filter=user_id_filter,
        start_date=start_date,
        end_date=end_date
    )

@inventory_bp.route('/audit-detail/<int:log_id>')
@login_required
def audit_detail(log_id):
    log = InventoryHistory.query.get_or_404(log_id)
    return jsonify(log.to_dict())

@inventory_bp.route('/alerts')
@login_required
def stock_alerts():
    tab = request.args.get('tab', 'low_stock', type=str)
    if tab not in ['low_stock', 'out_of_stock', 'expired', 'near_expiry']:
        tab = 'low_stock'

    search = request.args.get('search', '', type=str).strip()
    category_id = request.args.get('category_id', type=int)

    from app.models.category import Category
    all_categories = Category.query.filter_by(status='Active').order_by(Category.name).all()
    all_prods = Product.query.order_by(Product.name).all()

    low_stock_count = len([p for p in all_prods if p.is_low_stock()])
    out_of_stock_count = len([p for p in all_prods if p.is_out_of_stock()])
    expired_count = len([p for p in all_prods if p.is_expired()])
    near_expiry_count = len([p for p in all_prods if p.is_near_expiry()])

    if tab == 'out_of_stock':
        filtered = [p for p in all_prods if p.is_out_of_stock()]
    elif tab == 'expired':
        filtered = [p for p in all_prods if p.is_expired()]
    elif tab == 'near_expiry':
        filtered = [p for p in all_prods if p.is_near_expiry()]
    else:  # low_stock
        filtered = [p for p in all_prods if p.is_low_stock()]

    if category_id:
        filtered = [p for p in filtered if p.category_id == category_id]

    if search:
        s_lower = search.lower()
        filtered = [p for p in filtered if s_lower in p.name.lower() or s_lower in p.sku.lower()]

    return render_template(
        'inventory/stock_alerts.html',
        active_tab=tab,
        products=filtered,
        all_categories=all_categories,
        search=search,
        category_id=category_id,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count,
        expired_count=expired_count,
        near_expiry_count=near_expiry_count
    )
