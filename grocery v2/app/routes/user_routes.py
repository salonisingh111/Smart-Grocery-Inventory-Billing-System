from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app.database import db
from app.validators.forms import UserForm
from app.middleware.auth_middleware import admin_required
from app.services.auth_service import verify_sensitive_password

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    search = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '').strip()
    
    query = User.query
    if search:
        query = query.filter((User.full_name.ilike(f'%{search}%')) | (User.username.ilike(f'%{search}%')) | (User.email.ilike(f'%{search}%')))
    if role_filter:
        query = query.filter(User.role == role_filter)
        
    users = query.order_by(User.id.desc()).all()
    form = UserForm()
    return render_template('users/index.html', users=users, form=form, search=search, role_filter=role_filter)

@user_bp.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('user.index'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email address is already registered.', 'danger')
            return redirect(url_for('user.index'))
        
        pwd = form.password.data or 'grocery123'
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role=form.role.data,
            status=form.status.data
        )
        user.set_password(pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'User "{user.full_name}" created successfully.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', 'danger')
    return redirect(url_for('user.index'))

@user_bp.route('/<int:user_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit(user_id):
    user = User.query.get_or_404(user_id)
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    role = request.form.get('role')
    status = request.form.get('status')
    new_password = request.form.get('password')

    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if role and role in ['Admin', 'Manager', 'Cashier']:
        user.role = role
    if status and status in ['Active', 'Inactive']:
        user.status = status
    if new_password:
        user.set_password(new_password)

    db.session.commit()
    flash(f'User "{user.full_name}" updated successfully.', 'success')
    return redirect(url_for('user.index'))

@user_bp.route('/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_status(user_id):
    if current_user.id == user_id:
        flash('You cannot deactivate your own logged-in admin account.', 'warning')
        return redirect(url_for('user.index'))

    user = User.query.get_or_404(user_id)
    user.status = 'Inactive' if user.status == 'Active' else 'Active'
    db.session.commit()
    flash(f'Status for user "{user.full_name}" changed to {user.status}.', 'success')
    return redirect(url_for('user.index'))

@user_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(user_id):
    if current_user.id == user_id:
        flash('Action Denied: You cannot delete your own logged-in admin account.', 'danger')
        return redirect(url_for('user.index'))

    confirm_pwd = request.form.get('confirm_password')
    if not verify_sensitive_password(confirm_pwd):
        flash('Action Denied: Incorrect password confirmation for deleting user account.', 'danger')
        return redirect(url_for('user.index'))

    user = User.query.get_or_404(user_id)
    name = user.full_name
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{name}" deleted successfully.', 'success')
    return redirect(url_for('user.index'))
