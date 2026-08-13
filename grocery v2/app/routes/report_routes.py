from flask import Blueprint, render_template, request, jsonify, Response
from flask_login import login_required
from app.models.category import Category
from app.models.product import Product
from app.services.report_service import ReportService
from app.utils.logger import log_activity

report_bp = Blueprint('report', __name__, url_prefix='/reports')

def _get_filter_options():
    categories = Category.query.filter_by(status='Active').order_by(Category.name).all()
    products = Product.query.filter_by(status='Active').order_by(Product.name).all()
    payment_methods = ['Cash', 'UPI', 'Card']
    return {
        'all_categories': categories,
        'all_products': products,
        'all_payment_methods': payment_methods
    }

# -----------------------------------------------------------------------------
# SUBMODULE PAGE ROUTES
# -----------------------------------------------------------------------------

@report_bp.route('/')
@report_bp.route('/overview')
@login_required
def index():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    data = ReportService.get_overview_analytics(preset, start_date, end_date)
    ctx = _get_filter_options()
    return render_template(
        'reports/overview.html',
        active_tab='overview',
        data=data,
        filters=request.args,
        **ctx
    )

@report_bp.route('/overview_alias')
def overview():
    return index()


@report_bp.route('/sales')
@login_required
def sales():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    pay_method = request.args.get('payment_method')
    cat_id = request.args.get('category_id', type=int)

    data = ReportService.get_sales_analytics(preset, start_date, end_date, pay_method, cat_id)
    ctx = _get_filter_options()
    return render_template(
        'reports/sales.html',
        active_tab='sales',
        data=data,
        filters=request.args,
        **ctx
    )

@report_bp.route('/products')
@login_required
def products():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    cat_id = request.args.get('category_id', type=int)
    prod_id = request.args.get('product_id', type=int)

    data = ReportService.get_product_analytics(preset, start_date, end_date, cat_id, prod_id)
    ctx = _get_filter_options()
    return render_template(
        'reports/products.html',
        active_tab='products',
        data=data,
        filters=request.args,
        **ctx
    )

@report_bp.route('/customers')
@login_required
def customers():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    data = ReportService.get_customer_analytics(preset, start_date, end_date)
    ctx = _get_filter_options()
    return render_template(
        'reports/customers.html',
        active_tab='customers',
        data=data,
        filters=request.args,
        **ctx
    )

@report_bp.route('/finance')
@login_required
def finance():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    data = ReportService.get_finance_analytics(preset, start_date, end_date)
    ctx = _get_filter_options()
    return render_template(
        'reports/finance.html',
        active_tab='finance',
        data=data,
        filters=request.args,
        **ctx
    )

# -----------------------------------------------------------------------------
# JSON API ENDPOINTS FOR DYNAMIC DASHBOARD / FILTER UPDATES
# -----------------------------------------------------------------------------

@report_bp.route('/api/overview')
@login_required
def api_overview():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    data = ReportService.get_overview_analytics(preset, start_date, end_date)
    return jsonify(data)

@report_bp.route('/api/sales')
@login_required
def api_sales():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    pay_method = request.args.get('payment_method')
    cat_id = request.args.get('category_id', type=int)
    data = ReportService.get_sales_analytics(preset, start_date, end_date, pay_method, cat_id)
    return jsonify(data)

@report_bp.route('/api/products')
@login_required
def api_products():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    cat_id = request.args.get('category_id', type=int)
    prod_id = request.args.get('product_id', type=int)
    data = ReportService.get_product_analytics(preset, start_date, end_date, cat_id, prod_id)
    return jsonify(data)

@report_bp.route('/api/customers')
@login_required
def api_customers():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    data = ReportService.get_customer_analytics(preset, start_date, end_date)
    return jsonify(data)

@report_bp.route('/api/finance')
@login_required
def api_finance():
    preset = request.args.get('range_preset', 'this_month')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    data = ReportService.get_finance_analytics(preset, start_date, end_date)
    return jsonify(data)

# -----------------------------------------------------------------------------
# CSV EXPORT ROUTE
# -----------------------------------------------------------------------------

@report_bp.route('/export/<submodule>')
@login_required
def export_csv(submodule):
    if submodule not in ['overview', 'sales', 'products', 'customers', 'finance']:
        submodule = 'overview'
    csv_data, filename = ReportService.export_csv(submodule, request.args)
    log_activity('Export Report', f'Exported {submodule.capitalize()} analytics report data to CSV file ({filename})')
    response = Response(csv_data, mimetype="text/csv")
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


