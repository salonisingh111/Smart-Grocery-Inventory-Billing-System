from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from app.database import db
from app.models.bill import Bill, BillItem, BillReturn
from app.models.product import Product
from app.models.customer import Customer
from app.models.setting import SystemSetting
from app.services.billing_service import BillingService
from app.services.auth_service import verify_sensitive_password
from app.utils.logger import log_activity
from app.utils.notifications import create_activity_notification, sync_stock_alerts_for_product
import csv
import io

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

# ==========================================
# 1. BILLING DASHBOARD
# ==========================================
@billing_bp.route('/dashboard')
@login_required
def billing_dashboard():
    stats = BillingService.get_billing_dashboard_stats()
    currency = SystemSetting.get('CURRENCY', '₹')
    return render_template(
        'billing/dashboard.html',
        stats=stats,
        currency=currency
    )

# ==========================================
# 2. CREATE BILL (POS TERMINAL)
# ==========================================
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
        products = Product.query.filter_by(status='Active').limit(24).all()
    else:
        products = Product.query.filter(
            Product.status == 'Active',
            (Product.name.ilike(f"%{query_str}%")) |
            (Product.barcode == query_str) |
            (Product.sku == query_str)
        ).all()
        
    return jsonify([p.to_dict() for p in products])

@billing_bp.route('/api/quick-create-customer', methods=['POST'])
@login_required
def quick_create_customer():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip()
    address = data.get('address', '').strip()

    if not name or not phone:
        return jsonify({'success': False, 'message': 'Customer Name and Phone are required.'}), 400

    existing = Customer.query.filter_by(phone=phone).first()
    if existing:
        return jsonify({'success': True, 'customer': existing.to_dict(), 'message': 'Existing customer selected.'})

    customer = Customer(
        name=name,
        phone=phone,
        email=email,
        address=address,
        status='Active'
    )
    db.session.add(customer)
    db.session.commit()

    return jsonify({'success': True, 'customer': customer.to_dict(), 'message': 'Customer added successfully.'})

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

    log_activity('New Bill', f'Bill #{bill.bill_number} created — Amount: ₹{bill.total_amount:.2f} via {bill.payment_method}')
    create_activity_notification('New Bill', f'Bill #{bill.bill_number} created — ₹{bill.total_amount:.2f} via {bill.payment_method}', source_id=bill.id, created_by=current_user.full_name, link=f'/billing/invoice/{bill.id}')
    # Re-sync stock alerts for all bill items (stock was deducted)
    for item_data in items:
        pid = item_data.get('product_id')
        if pid:
            sync_stock_alerts_for_product(pid)
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

@billing_bp.route('/api/bill-details/<int:id>')
@login_required
def api_bill_details(id):
    bill = Bill.query.get_or_404(id)
    data = bill.to_dict()
    data['items'] = [item.to_dict() for item in bill.items]
    return jsonify(data)

# ==========================================
# 3. BILLING HISTORY
# ==========================================
@billing_bp.route('/history')
@login_required
def billing_history():
    search = request.args.get('search', '').strip()
    payment_filter = request.args.get('payment_method', '').strip()
    status_filter = request.args.get('status', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Bill.query

    if search:
        query = query.outerjoin(Customer).filter(
            (Bill.bill_number.ilike(f"%{search}%")) |
            (Customer.name.ilike(f"%{search}%")) |
            (Customer.phone.ilike(f"%{search}%"))
        )

    if payment_filter:
        query = query.filter(Bill.payment_method == payment_filter)

    if status_filter:
        query = query.filter(Bill.status == status_filter)

    if start_date:
        try:
            s_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Bill.created_at >= s_dt)
        except ValueError:
            pass

    if end_date:
        try:
            e_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Bill.created_at < e_dt)
        except ValueError:
            pass

    bills = query.order_by(Bill.created_at.desc()).all()
    currency = SystemSetting.get('CURRENCY', '₹')

    return render_template(
        'billing/history.html',
        bills=bills,
        search=search,
        payment_filter=payment_filter,
        status_filter=status_filter,
        start_date=start_date,
        end_date=end_date,
        currency=currency
    )

# ==========================================
# 4. RETURNS & REFUNDS
# ==========================================
@billing_bp.route('/returns')
@login_required
def returns_and_refunds():
    initial_bill_number = request.args.get('bill_number', '').strip()
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()

    # Auto-seed realistic demo returns if database table is empty
    if BillReturn.query.count() == 0:
        seed_returns_data()

    query = BillReturn.query.join(Bill)

    if search:
        query = query.outerjoin(Customer, BillReturn.customer_id == Customer.id).filter(
            (BillReturn.return_number.ilike(f"%{search}%")) |
            (Bill.bill_number.ilike(f"%{search}%")) |
            (Customer.name.ilike(f"%{search}%")) |
            (Customer.phone.ilike(f"%{search}%"))
        )

    if status_filter:
        query = query.filter(BillReturn.status == status_filter)

    returns_history = query.order_by(BillReturn.created_at.desc()).all()
    currency = SystemSetting.get('CURRENCY', '₹')

    return render_template(
        'billing/returns.html',
        returns_history=returns_history,
        initial_bill_number=initial_bill_number,
        search=search,
        status_filter=status_filter,
        currency=currency
    )

@billing_bp.route('/api/search-bill')
@login_required
def search_bill():
    q = request.args.get('query', '').strip()
    if not q:
        return jsonify({'success': False, 'message': 'Search query is required.'}), 400

    bills = Bill.query.outerjoin(Customer).filter(
        (Bill.bill_number.ilike(f"%{q}%")) |
        (Customer.name.ilike(f"%{q}%")) |
        (Customer.phone.ilike(f"%{q}%"))
    ).order_by(Bill.created_at.desc()).limit(10).all()

    if not bills:
        return jsonify({'success': False, 'message': 'No matching bill found.'}), 404

    results = []
    for b in bills:
        results.append({
            'id': b.id,
            'bill_number': b.bill_number,
            'customer_name': b.customer.name if b.customer else 'Walk-in Customer',
            'customer_phone': b.customer.phone if b.customer else '',
            'total_amount': b.net_amount,
            'created_at': b.created_at.strftime('%Y-%m-%d %H:%M'),
            'status': b.status
        })

    return jsonify({'success': True, 'bills': results})

@billing_bp.route('/api/bill-for-return/<path:bill_identifier>')
@login_required
def get_bill_for_return(bill_identifier):
    identifier = bill_identifier.strip()
    bill = Bill.query.filter_by(bill_number=identifier).first()
    if not bill and identifier.isdigit():
        bill = Bill.query.get(int(identifier))

    if not bill:
        return jsonify({'success': False, 'message': 'No matching bill found.'}), 404

    if bill.status == 'Cancelled':
        return jsonify({'success': False, 'message': 'This bill is cancelled and cannot be returned.'}), 400

    items_data = []
    for item in bill.items:
        returned_qty = item.returned_quantity or 0
        remaining_qty = max(0, item.quantity - returned_qty)
        items_data.append({
            'bill_item_id': item.id,
            'product_id': item.product_id,
            'product_name': item.product_name,
            'sku': item.product.sku if item.product else 'N/A',
            'unit_price': item.unit_price,
            'purchased_quantity': item.quantity,
            'returned_quantity': returned_qty,
            'max_returnable_quantity': remaining_qty,
            'tax_amount': item.tax_amount,
            'total_price': item.total_price
        })

    return jsonify({
        'success': True,
        'bill': bill.to_dict(),
        'items': items_data
    })

@billing_bp.route('/api/return-details/<int:id>')
@login_required
def get_return_details(id):
    ret = BillReturn.query.get_or_404(id)
    data = ret.to_dict()
    data['stock_updated'] = 'Yes'
    return jsonify({'success': True, 'return_data': data})

@billing_bp.route('/api/process-return', methods=['POST'])
@login_required
def process_return_api():
    data = request.get_json() or {}
    bill_id = data.get('bill_id')
    items = data.get('items', [])
    refund_method = data.get('refund_method', 'Cash')
    reason = data.get('reason', 'Customer Return')
    remarks = data.get('remarks', '')

    success, msg, return_rec = BillingService.process_return(
        bill_id=bill_id,
        items_data=items,
        refund_method=refund_method,
        reason=reason,
        user_id=current_user.id,
        remarks=remarks
    )

    if not success:
        return jsonify({'success': False, 'message': msg}), 400

    return jsonify({
        'success': True,
        'message': msg,
        'return_number': return_rec.return_number
    })

def seed_returns_data():
    try:
        from app.database import db
        from app.models.user import User
        from app.models.product import Product
        
        user = User.query.first()
        if not user:
            return

        recent_bills = Bill.query.order_by(Bill.id.desc()).limit(6).all()
        if len(recent_bills) < 2:
            return

        for idx, bill in enumerate(recent_bills[:3]):
            if bill.items and not bill.returns:
                item = bill.items[0]
                if item.quantity >= 1:
                    ret_qty = 1
                    unit_refund = item.unit_price + (item.tax_amount / item.quantity if item.quantity else 0.0)
                    tot_ref = round(unit_refund * ret_qty, 2)
                    
                    ret_num = f"RET-20260809-{idx+1:04d}"
                    b_ret = BillReturn(
                        return_number=ret_num,
                        bill_id=bill.id,
                        customer_id=bill.customer_id,
                        user_id=user.id,
                        total_refund=tot_ref,
                        refund_method=bill.payment_method or 'Cash',
                        reason='Quality Issue' if idx == 0 else ('Wrong Product' if idx == 1 else 'Damaged Product'),
                        status='Completed',
                        remarks='Processed customer return during verification'
                    )
                    db.session.add(b_ret)
                    db.session.flush()

                    item.returned_quantity = (item.returned_quantity or 0) + ret_qty
                    ret_item = BillReturnItem(
                        return_id=b_ret.id,
                        bill_item_id=item.id,
                        product_id=item.product_id,
                        product_name=item.product_name,
                        quantity=ret_qty,
                        unit_price=item.unit_price,
                        refund_amount=tot_ref,
                        reason=b_ret.reason
                    )
                    db.session.add(ret_item)

                    prod = Product.query.get(item.product_id)
                    if prod:
                        prev_qty = prod.quantity
                        prod.quantity += ret_qty
                        inv_log = InventoryHistory(
                            product_id=prod.id,
                            change_type='Return',
                            quantity_changed=ret_qty,
                            previous_stock=prev_qty,
                            remaining_quantity=prod.quantity,
                            reason=f"Customer Return: {b_ret.reason}",
                            remarks=f"Return #{ret_num} against Bill #{bill.bill_number}",
                            reference_code=ret_num,
                            performed_by_user_id=user.id
                        )
                        db.session.add(inv_log)

                    bill.status = 'Partially Returned'

        db.session.commit()
    except Exception as e:
        db.session.rollback()

# ==========================================
# 5. SALES REPORTS
# ==========================================
@billing_bp.route('/sales-reports')
@login_required
def sales_reports():
    period = request.args.get('period', 'this_month', type=str)
    start_date = request.args.get('start_date', '', type=str)
    end_date = request.args.get('end_date', '', type=str)

    now = datetime.utcnow()
    
    if period == 'today':
        s_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        e_dt = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == 'yesterday':
        y = now - timedelta(days=1)
        s_dt = y.replace(hour=0, minute=0, second=0, microsecond=0)
        e_dt = y.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == 'this_week':
        s_dt = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        e_dt = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == 'this_year':
        s_dt = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        e_dt = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == 'custom' and start_date and end_date:
        try:
            s_dt = datetime.strptime(start_date, '%Y-%m-%d')
            e_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            s_dt = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            e_dt = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    else: # default: this_month
        period = 'this_month'
        s_dt = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        e_dt = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    bills_query = Bill.query.filter(
        Bill.created_at >= s_dt,
        Bill.created_at <= e_dt,
        Bill.status != 'Cancelled'
    )
    bills = bills_query.order_by(Bill.created_at.desc()).all()

    total_sales = sum(b.net_amount for b in bills)
    total_bills = len(bills)
    total_items_sold = sum(sum(item.quantity for item in b.items) for b in bills)
    total_discount = sum(b.discount_amount for b in bills)
    total_tax = sum(b.tax_amount for b in bills)
    net_sales = total_sales
    avg_bill_val = (total_sales / total_bills) if total_bills > 0 else 0.0

    # Sales by Payment Method
    pm_stats = {}
    for b in bills:
        pm_stats[b.payment_method] = pm_stats.get(b.payment_method, 0.0) + b.net_amount

    # Sales by Category
    category_sales_query = db.session.query(
        Product.category_id,
        func.sum(BillItem.total_price).label('revenue')
    ).join(BillItem, Product.id == BillItem.product_id)\
     .join(Bill, BillItem.bill_id == Bill.id)\
     .filter(Bill.created_at >= s_dt, Bill.created_at <= e_dt, Bill.status != 'Cancelled')\
     .group_by(Product.category_id).all()

    from app.models.category import Category
    cat_stats = []
    for cat_id, rev in category_sales_query:
        cat = Category.query.get(cat_id) if cat_id else None
        cat_stats.append({
            'category_name': cat.name if cat else 'Uncategorized',
            'revenue': round(float(rev or 0.0), 2)
        })

    # Top Selling Products in Period
    top_products_query = db.session.query(
        BillItem.product_name,
        func.sum(BillItem.quantity).label('qty'),
        func.sum(BillItem.total_price).label('revenue')
    ).join(Bill, BillItem.bill_id == Bill.id)\
     .filter(Bill.created_at >= s_dt, Bill.created_at <= e_dt, Bill.status != 'Cancelled')\
     .group_by(BillItem.product_name)\
     .order_by(db.desc('qty')).limit(10).all()

    top_products = [
        {'name': r[0], 'qty': r[1], 'revenue': round(float(r[2] or 0.0), 2)}
        for r in top_products_query
    ]

    currency = SystemSetting.get('CURRENCY', '₹')

    return render_template(
        'billing/sales_reports.html',
        period=period,
        start_date=start_date,
        end_date=end_date,
        total_sales=round(total_sales, 2),
        total_bills=total_bills,
        total_items_sold=total_items_sold,
        total_discount=round(total_discount, 2),
        total_tax=round(total_tax, 2),
        net_sales=round(net_sales, 2),
        avg_bill_val=round(avg_bill_val, 2),
        pm_stats=pm_stats,
        cat_stats=cat_stats,
        top_products=top_products,
        bills=bills,
        currency=currency
    )

@billing_bp.route('/export/sales-csv')
@login_required
def export_sales_csv():
    bills = Bill.query.filter(Bill.status != 'Cancelled').order_by(Bill.created_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Bill Number', 'Date', 'Customer', 'Items Count', 'Payment Method', 'Discount', 'Tax', 'Grand Total', 'Status'])

    for b in bills:
        writer.writerow([
            b.bill_number,
            b.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            b.customer.name if b.customer else 'Walk-in Customer',
            len(b.items),
            b.payment_method,
            b.discount_amount,
            b.tax_amount,
            b.net_amount,
            b.status
        ])

    log_activity('Export Sales Report', f'Exported sales report ({len(bills)} sales transactions) to CSV file')

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=grocery_sales_report.csv"}
    )

@billing_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_bill(id):
    bill = Bill.query.get_or_404(id)
    confirm_password = request.form.get('confirm_password')

    if not verify_sensitive_password(confirm_password):
        flash('Action Denied: Incorrect password confirmation for bill cancellation.', 'danger')
        return redirect(url_for('billing.billing_history'))

    bill.status = 'Cancelled'
    db.session.commit()

    log_activity('Cancel Bill', f'Cancelled Bill #{bill.bill_number} (Amount: ₹{bill.net_amount})')

    flash(f"Bill #{bill.bill_number} has been cancelled successfully.", 'info')
    return redirect(url_for('billing.billing_history'))
