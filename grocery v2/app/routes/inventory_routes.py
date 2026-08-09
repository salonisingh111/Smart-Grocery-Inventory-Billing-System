from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.inventory import InventoryHistory
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
    products = Product.query.order_by(Product.name).all()

    if form.validate_on_submit():
        if not verify_sensitive_password(form.confirm_password.data):
            flash('Action Denied: Incorrect password confirmation for inventory adjustment.', 'danger')
            return redirect(url_for('inventory.index'))

        product_id = request.form.get('product_id', type=int)
        qty_change = form.quantity_changed.data
        if form.change_type.data == 'Stock Out':
            qty_change = -abs(qty_change)

        success, msg = InventoryService.adjust_stock(
            product_id=product_id,
            quantity_change=qty_change,
            change_type=form.change_type.data,
            reason=form.reason.data,
            user_id=current_user.id
        )

        if success:
            product = Product.query.get(product_id)
            pname = product.name if product else f'ID#{product_id}'
            log_activity('Stock Adjustment', f'{form.change_type.data}: {abs(form.quantity_changed.data)} units of "{pname}" — {form.reason.data or "No reason given"}')
            create_activity_notification('Stock Adjustment', f'{form.change_type.data}: {abs(form.quantity_changed.data)} units of "{pname}"', created_by=current_user.full_name)
            sync_stock_alerts_for_product(product_id)
            flash(msg, 'success')
        else:
            flash(msg, 'danger')

        return redirect(url_for('inventory.index'))

    search = request.args.get('search', '', type=str)
    query = InventoryHistory.query

    if search:
        query = query.join(Product).filter((Product.name.like(f"%{search}%")) | (InventoryHistory.reason.like(f"%{search}%")))

    logs = query.order_by(InventoryHistory.created_at.desc()).all()

    return render_template('inventory/index.html', logs=logs, products=products, form=form, search=search)
