from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.bill import Bill
from app.models.product import Product
from app.models.customer import Customer
from app.models.setting import SystemSetting
from app.services.billing_service import BillingService
from app.services.auth_service import verify_sensitive_password

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

@billing_bp.route('/pos')
@login_required
def pos():
    products = Product.query.filter_by(status='Active').all()
    customers = Customer.query.filter_by(status='Active').all()
    currency = SystemSetting.get('CURRENCY', '₹')
    default_tax = float(SystemSetting.get('TAX_PERCENTAGE', '5.0'))
    
    return render_template(
        'billing/pos.html',
        products=[p.to_dict() for p in products],
        customers=customers,
        currency=currency,
        default_tax=default_tax
    )

@billing_bp.route('/api/search-products')
@login_required
def search_products():
    query_str = request.args.get('q', '', type=str)
    if not query_str:
        products = Product.query.filter_by(status='Active').limit(20).all()
    else:
        products = Product.query.filter(
            Product.status == 'Active',
            (Product.name.like(f"%{query_str}%")) |
            (Product.barcode == query_str) |
            (Product.sku == query_str)
        ).all()
        
    return jsonify([p.to_dict() for p in products])

@billing_bp.route('/api/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.get_json() or {}
    customer_id = data.get('customer_id')
    items = data.get('items', [])
    payment_method = data.get('payment_method', 'Cash')
    discount_amount = float(data.get('discount_amount', 0.0))
    notes = data.get('notes', '')

    success, msg, bill = BillingService.create_checkout_bill(
        customer_id=customer_id,
        items_data=items,
        payment_method=payment_method,
        discount_amount=discount_amount,
        notes=notes,
        user_id=current_user.id
    )

    if not success:
        return jsonify({'success': False, 'message': msg}), 400

    return jsonify({
        'success': True,
        'message': msg,
        'bill_id': bill.id,
        'bill_number': bill.bill_number
    })

@billing_bp.route('/invoice/<int:id>')
@login_required
def view_invoice(id):
    bill = Bill.query.get_or_404(id)
    store_name = SystemSetting.get('STORE_NAME', 'Smart Grocery Store')
    store_gst = SystemSetting.get('GST_NUMBER', 'GSTIN9988776655')
    store_phone = SystemSetting.get('STORE_PHONE', '+91 98765 43210')
    store_email = SystemSetting.get('STORE_EMAIL', 'info@smartgrocery.com')
    currency = SystemSetting.get('CURRENCY', '₹')

    return render_template(
        'billing/invoice.html',
        bill=bill,
        store_name=store_name,
        store_gst=store_gst,
        store_phone=store_phone,
        store_email=store_email,
        currency=currency
    )

@billing_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_bill(id):
    bill = Bill.query.get_or_404(id)
    confirm_password = request.form.get('confirm_password')

    if not verify_sensitive_password(confirm_password):
        flash('Action Denied: Incorrect password confirmation for bill deletion.', 'danger')
        return redirect(url_for('dashboard.index'))

    bill.status = 'Cancelled'
    from app.database import db
    db.session.commit()

    flash(f"Bill #{bill.bill_number} has been cancelled successfully.", 'info')
    return redirect(url_for('dashboard.index'))
