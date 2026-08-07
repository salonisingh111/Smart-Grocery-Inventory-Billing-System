from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.database import db
from app.models.category import Category
from app.validators.forms import CategoryForm
from app.services.auth_service import verify_sensitive_password

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CategoryForm()
    search = request.args.get('search', '', type=str)

    if form.validate_on_submit():
        if Category.query.filter_by(name=form.name.data).first():
            flash('Category name already exists.', 'danger')
        elif Category.query.filter_by(code=form.code.data).first():
            flash('Category code already exists.', 'danger')
        else:
            category = Category(
                name=form.name.data,
                code=form.code.data.upper(),
                description=form.description.data,
                status=form.status.data
            )
            db.session.add(category)
            db.session.commit()
            flash(f"Category '{category.name}' created successfully!", 'success')
            return redirect(url_for('category.index'))

    query = Category.query
    if search:
        query = query.filter((Category.name.like(f"%{search}%")) | (Category.code.like(f"%{search}%")))

    categories = query.order_by(Category.name).all()
    return render_template('categories/index.html', categories=categories, form=form, search=search)

@category_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    category = Category.query.get_or_404(id)
    name = request.form.get('name')
    code = request.form.get('code')
    description = request.form.get('description')
    status = request.form.get('status', 'Active')

    if not name or not code:
        flash('Category Name and Code are required.', 'danger')
        return redirect(url_for('category.index'))

    category.name = name
    category.code = code.upper()
    category.description = description
    category.status = status
    db.session.commit()

    flash(f"Category '{category.name}' updated successfully.", 'success')
    return redirect(url_for('category.index'))

@category_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    category = Category.query.get_or_404(id)
    confirm_password = request.form.get('confirm_password')

    # Prevent deletion if products exist
    if category.products and len(category.products) > 0:
        flash(f"Cannot delete category '{category.name}': {len(category.products)} products are assigned to it. Reassign or delete those products first.", 'warning')
        return redirect(url_for('category.index'))

    if not verify_sensitive_password(confirm_password):
        flash('Action Denied: Incorrect password confirmation for category deletion.', 'danger')
        return redirect(url_for('category.index'))

    cat_name = category.name
    db.session.delete(category)
    db.session.commit()

    flash(f"Category '{cat_name}' deleted successfully.", 'info')
    return redirect(url_for('category.index'))
