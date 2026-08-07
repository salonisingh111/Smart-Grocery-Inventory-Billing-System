from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.database import db
from app.models.customer import Customer
from app.validators.forms import CustomerForm
from app.services.auth_service import verify_sensitive_password

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CustomerForm()
    search = request.args.get('search', '', type=str)

    if form.validate_on_submit():
        if Customer.query.filter_by(phone=form.phone.data).first():
            flash('Customer with this phone number already exists.', 'danger')
        else:
            customer = Customer(
                name=form.name.data,
                phone=form.phone.data,
                email=form.email.data or None,
                address=form.address.data or None,
                status=form.status.data
            )
            db.session.add(customer)
            db.session.commit()
            flash(f"Customer '{customer.name}' registered successfully!", 'success')
            return redirect(url_for('customer.index'))

    query = Customer.query
    if search:
        query = query.filter(
            (Customer.name.like(f"%{search}%")) |
            (Customer.phone.like(f"%{search}%")) |
            (Customer.email.like(f"%{search}%"))
        )

    customers = query.order_by(Customer.created_at.desc()).all()
    return render_template('customers/index.html', customers=customers, form=form, search=search)

@customer_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    customer = Customer.query.get_or_404(id)
    customer.name = request.form.get('name')
    customer.phone = request.form.get('phone')
    customer.email = request.form.get('email')
    customer.address = request.form.get('address')
    customer.status = request.form.get('status', 'Active')

    db.session.commit()
    flash(f"Customer '{customer.name}' updated successfully.", 'success')
    return redirect(url_for('customer.index'))

@customer_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    customer = Customer.query.get_or_404(id)
    confirm_password = request.form.get('confirm_password')

    if not verify_sensitive_password(confirm_password):
        flash('Action Denied: Incorrect password confirmation for customer deletion.', 'danger')
        return redirect(url_for('customer.index'))

    cust_name = customer.name
    db.session.delete(customer)
    db.session.commit()

    flash(f"Customer '{cust_name}' deleted successfully.", 'info')
    return redirect(url_for('customer.index'))
