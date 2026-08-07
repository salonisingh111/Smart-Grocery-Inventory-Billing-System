from flask import Blueprint, render_template, request, Response
from flask_login import login_required
from app.models.bill import Bill
from app.models.product import Product
from app.models.customer import Customer
from app.models.supplier import Supplier
from app.services.report_service import ReportService

report_bp = Blueprint('report', __name__, url_prefix='/reports')

@report_bp.route('/')
@login_required
def index():
    report_type = request.args.get('type', 'sales', type=str)
    start_date = request.args.get('start_date', '', type=str)
    end_date = request.args.get('end_date', '', type=str)

    bills = []
    products = []
    customers = []
    suppliers = []

    if report_type == 'sales':
        bills = Bill.query.order_by(Bill.created_at.desc()).all()
    elif report_type == 'inventory' or report_type == 'stock':
        products = Product.query.order_by(Product.name).all()
    elif report_type == 'low_stock':
        products = [p for p in Product.query.all() if p.is_low_stock()]
    elif report_type == 'expired':
        products = [p for p in Product.query.all() if p.is_expired()]
    elif report_type == 'customer':
        customers = Customer.query.order_by(Customer.total_purchases.desc()).all()
    elif report_type == 'supplier':
        suppliers = Supplier.query.order_by(Supplier.name).all()

    return render_template(
        'reports/index.html',
        report_type=report_type,
        bills=bills,
        products=products,
        customers=customers,
        suppliers=suppliers,
        start_date=start_date,
        end_date=end_date
    )

@report_bp.route('/export/sales')
@login_required
def export_sales():
    csv_data = ReportService.generate_sales_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=sales_report.csv"}
    )

@report_bp.route('/export/inventory')
@login_required
def export_inventory():
    csv_data = ReportService.generate_inventory_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=inventory_report.csv"}
    )
