import csv
import io
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, Response
from flask_login import login_required, current_user
from app.database import db
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.validators.forms import ProductForm
from app.services.auth_service import verify_sensitive_password
from app.utils.helpers import save_uploaded_image

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category_id', type=int)
    stock_status = request.args.get('stock_status', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Product.query

    if search:
        query = query.filter(
            (Product.name.like(f"%{search}%")) |
            (Product.sku.like(f"%{search}%")) |
            (Product.barcode.like(f"%{search}%")) |
            (Product.brand.like(f"%{search}%"))
        )

    if category_id:
        query = query.filter_by(category_id=category_id)

    all_items = query.order_by(Product.name).all()

    if stock_status == 'low':
        items = [p for p in all_items if p.is_low_stock()]
    elif stock_status == 'out':
        items = [p for p in all_items if p.is_out_of_stock()]
    elif stock_status == 'expired':
        items = [p for p in all_items if p.is_expired()]
    else:
        items = all_items

    # Manual Pagination calculation for filtered lists
    total_count = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = items[start:end]
    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1

    categories = Category.query.filter_by(status='Active').all()

    return render_template(
        'products/index.html',
        products=paginated_products,
        categories=categories,
        search=search,
        selected_category=category_id,
        stock_status=stock_status,
        page=page,
        total_pages=total_pages,
        total_count=total_count
    )

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(status='Active').all()]
    suppliers = [(s.id, s.name) for s in Supplier.query.filter_by(status='Active').all()]
    form.supplier_id.choices = [(0, 'Select Supplier (Optional)')] + suppliers

    if form.validate_on_submit():
        sku_val = form.sku.data.strip() if form.sku.data else ''
        if not sku_val and SystemSetting.get_bool('AUTO_GENERATE_SKU', True):
            import time
            sku_val = f"SKU-{int(time.time())}"

        if sku_val and Product.query.filter_by(sku=sku_val).first():
            flash('Product SKU code already exists. Please use a unique SKU.', 'danger')
            return render_template('products/form.html', form=form, title='Add New Product')

        image_path = None
        if form.image.data:
            image_path = save_uploaded_image(form.image.data, folder_name='products')

        product = Product(
            name=form.name.data,
            sku=sku_val or f"SKU-{int(time.time())}",
            barcode=form.barcode.data or None,
            category_id=form.category_id.data,
            supplier_id=form.supplier_id.data if form.supplier_id.data != 0 else None,
            brand=form.brand.data or None,
            purchase_price=form.purchase_price.data,
            selling_price=form.selling_price.data,
            tax_percent=form.tax_percent.data or 0.0,
            discount_percent=form.discount_percent.data or 0.0,
            quantity=form.quantity.data,
            min_stock=form.min_stock.data,
            max_stock=form.max_stock.data,
            expiry_date=form.expiry_date.data,
            mfd_date=form.mfd_date.data,
            unit=form.unit.data,
            image=image_path,
            status=form.status.data,
            notes=form.notes.data
        )

        db.session.add(product)
        db.session.commit()

        flash(f"Product '{product.name}' added successfully!", 'success')
        return redirect(url_for('product.index'))

    return render_template('products/form.html', form=form, title='Add New Product')

@product_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(status='Active').all()]
    suppliers = [(s.id, s.name) for s in Supplier.query.filter_by(status='Active').all()]
    form.supplier_id.choices = [(0, 'Select Supplier (Optional)')] + suppliers

    if request.method == 'GET':
        form.supplier_id.data = product.supplier_id or 0

    if form.validate_on_submit():
        # Check price change sensitive password requirement
        if form.selling_price.data != product.selling_price:
            confirm_pwd = request.form.get('confirm_password')
            if not confirm_pwd or not verify_sensitive_password(confirm_pwd):
                flash('Password verification required to change Product Selling Price.', 'danger')
                return render_template('products/form.html', form=form, title=f"Edit Product: {product.name}", product=product)

        if form.image.data:
            img_path = save_uploaded_image(form.image.data, folder_name='products')
            if img_path:
                product.image = img_path

        product.name = form.name.data
        product.sku = form.sku.data
        product.barcode = form.barcode.data or None
        product.category_id = form.category_id.data
        product.supplier_id = form.supplier_id.data if form.supplier_id.data != 0 else None
        product.brand = form.brand.data or None
        product.purchase_price = form.purchase_price.data
        product.selling_price = form.selling_price.data
        product.tax_percent = form.tax_percent.data or 0.0
        product.discount_percent = form.discount_percent.data or 0.0
        product.quantity = form.quantity.data
        product.min_stock = form.min_stock.data
        product.max_stock = form.max_stock.data
        product.expiry_date = form.expiry_date.data
        product.mfd_date = form.mfd_date.data
        product.unit = form.unit.data
        product.status = form.status.data
        product.notes = form.notes.data

        db.session.commit()
        flash(f"Product '{product.name}' updated successfully!", 'success')
        return redirect(url_for('product.index'))

    return render_template('products/form.html', form=form, title=f"Edit Product: {product.name}", product=product)

@product_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    confirm_password = request.form.get('confirm_password')

    if not verify_sensitive_password(confirm_password):
        flash('Action Denied: Incorrect password confirmation for product deletion.', 'danger')
        return redirect(url_for('product.index'))

    prod_name = product.name
    db.session.delete(product)
    db.session.commit()

    flash(f"Product '{prod_name}' deleted successfully.", 'info')
    return redirect(url_for('product.index'))

@product_bp.route('/export/csv')
@login_required
def export_csv():
    products = Product.query.all()
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(['ID', 'Name', 'SKU', 'Barcode', 'Category', 'Brand', 'Purchase Price', 'Selling Price', 'Tax %', 'Quantity', 'Min Stock', 'Unit', 'Status'])

    for p in products:
        writer.writerow([
            p.id, p.name, p.sku, p.barcode or '', p.category.name if p.category else '',
            p.brand or '', p.purchase_price, p.selling_price, p.tax_percent,
            p.quantity, p.min_stock, p.unit, p.status
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=grocery_products.csv"}
    )
