from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.validators.forms import LoginForm
from app.database import db
from app.utils.logger import log_activity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username.data) | (User.email == form.username.data)).first()
        if user and user.check_password(form.password.data):
            if user.status != 'Active':
                log_activity('Failed Login Attempt', f'Deactivated user "{form.username.data}" attempted login', user_id=user.id, user_name=user.full_name)
                flash('Your account has been deactivated. Contact Admin.', 'danger')
                return render_template('auth/login.html', form=form)
            
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if client_ip and ',' in client_ip:
                client_ip = client_ip.split(',')[0].strip()

            user.last_login_at = datetime.utcnow()
            user.last_login_ip = client_ip
            db.session.commit()

            login_user(user, remember=form.remember_me.data)
            log_activity('User Login', f'User logged in successfully (Role: {user.role})', user_id=user.id, user_name=user.full_name)

            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            log_activity('Failed Login Attempt', f'Invalid login attempt for username "{form.username.data}"')
            flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    log_activity('User Logout', f'User logged out (ID: {current_user.id})')
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('auth.login'))
