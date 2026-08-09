from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.database import db
from app.models.supplier import Supplier
from app.validators.forms import SupplierForm
from app.services.auth_service import verify_sensitive_password
from app.utils.logger import log_activity
from app.utils.notifications import create_activity_notification

supplier_bp = Blueprint('supplier', __name__, url_prefix='/suppliers')

@supplier_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SupplierForm()
    search = request.args.get('search', '', type=str)

    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data or None,
            gst_number=form.gst_number.data or None,
            address=form.address.data or None,
            status=form.status.data
        )
        db.session.add(supplier)
        db.session.commit()
        log_activity('Add Supplier', f'Supplier "{supplier.name}" added (Phone: {supplier.phone})')
        create_activity_notification('Add Supplier', f'Supplier "{supplier.name}" added (Phone: {supplier.phone})', created_by=current_user.full_name)
        flash(f"Supplier '{supplier.name}' added successfully!", 'success')
        return redirect(url_for('supplier.index'))

    query = Supplier.query
    if search:
        query = query.filter(
            (Supplier.name.like(f"%{search}%")) |
            (Supplier.phone.like(f"%{search}%")) |
            (Supplier.email.like(f"%{search}%"))
        )

    suppliers = query.order_by(Supplier.name).all()
    return render_template('suppliers/index.html', suppliers=suppliers, form=form, search=search)

@supplier_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    supplier = Supplier.query.get_or_404(id)
    supplier.name = request.form.get('name')
    supplier.phone = request.form.get('phone')
    supplier.email = request.form.get('email')
    supplier.gst_number = request.form.get('gst_number')
    supplier.address = request.form.get('address')
    supplier.status = request.form.get('status', 'Active')

    db.session.commit()
    log_activity('Edit Supplier', f'Supplier "{supplier.name}" updated')
    create_activity_notification('Edit Supplier', f'Supplier "{supplier.name}" updated', created_by=current_user.full_name)
    flash(f"Supplier '{supplier.name}' updated successfully.", 'success')
    return redirect(url_for('supplier.index'))

@supplier_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    supplier = Supplier.query.get_or_404(id)
    confirm_password = request.form.get('confirm_password')

    if not verify_sensitive_password(confirm_password):
        flash('Action Denied: Incorrect password confirmation for supplier deletion.', 'danger')
        return redirect(url_for('supplier.index'))

    sup_name = supplier.name
    db.session.delete(supplier)
    db.session.commit()
    log_activity('Delete Supplier', f'Supplier "{sup_name}" deleted')
    create_activity_notification('Delete Supplier', f'Supplier "{sup_name}" deleted', created_by=current_user.full_name)
    flash(f"Supplier '{sup_name}' deleted successfully.", 'info')
    return redirect(url_for('supplier.index'))
