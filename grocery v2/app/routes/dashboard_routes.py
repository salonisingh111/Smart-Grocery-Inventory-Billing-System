from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from sqlalchemy import func
from app.models.bill import Bill
from app.models.product import Product
from app.models.customer import Customer
from app.models.category import Category
from app.models.inventory import InventoryHistory

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    today = datetime.utcnow().date()
    start_of_month = datetime(today.year, today.month, 1)

    # Today's Sales & Count
    today_bills = Bill.query.filter(
        func.date(Bill.created_at) == today,
        Bill.status == 'Paid'
    ).all()
    todays_sales = sum(b.net_amount for b in today_bills)

    # Monthly Sales & Total Revenue
    monthly_bills = Bill.query.filter(
        Bill.created_at >= start_of_month,
        Bill.status == 'Paid'
    ).all()
    monthly_sales = sum(b.net_amount for b in monthly_bills)

    all_paid_bills = Bill.query.filter_by(status='Paid').all()
    total_revenue = sum(b.net_amount for b in all_paid_bills)

    # Product metrics
    total_products = Product.query.count()
    all_products = Product.query.all()
    low_stock_count = sum(1 for p in all_products if p.is_low_stock())
    out_of_stock_count = sum(1 for p in all_products if p.is_out_of_stock())
    expired_count = sum(1 for p in all_products if p.is_expired())

    # Recent lists
    recent_bills = Bill.query.order_by(Bill.created_at.desc()).limit(5).all()
    recent_customers = Customer.query.order_by(Customer.created_at.desc()).limit(5).all()
    latest_inventory_logs = InventoryHistory.query.order_by(InventoryHistory.created_at.desc()).limit(6).all()

    return render_template(
        'dashboard/index.html',
        todays_sales=todays_sales,
        monthly_sales=monthly_sales,
        total_revenue=total_revenue,
        total_products=total_products,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count,
        expired_count=expired_count,
        recent_bills=recent_bills,
        recent_customers=recent_customers,
        latest_inventory_logs=latest_inventory_logs
    )

@dashboard_bp.route('/api/dashboard/chart-data')
@login_required
def chart_data():
    # 7-day Sales & Revenue data
    today = datetime.utcnow().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    sales_labels = [d.strftime('%b %d') for d in dates]
    sales_values = []
    revenue_values = []

    for d in dates:
        bills = Bill.query.filter(
            func.date(Bill.created_at) == d,
            Bill.status == 'Paid'
        ).all()
        sales_values.append(len(bills))
        revenue_values.append(sum(b.net_amount for b in bills))

    # Category distribution
    categories = Category.query.all()
    cat_labels = [c.name for c in categories]
    cat_values = [len(c.products) for c in categories]

    return jsonify({
        'sales': {
            'labels': sales_labels,
            'values': sales_values,
            'revenue': revenue_values
        },
        'categories': {
            'labels': cat_labels,
            'values': cat_values
        }
    })
