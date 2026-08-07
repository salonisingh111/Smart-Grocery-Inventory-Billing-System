from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.database import db
from app.validators.forms import ProfileForm
from app.utils.helpers import save_uploaded_image

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        if form.new_password.data:
            if not form.current_password.data or not current_user.check_password(form.current_password.data):
                flash('Current password is required to set a new password.', 'danger')
                return render_template('profile/index.html', form=form)
            
            current_user.set_password(form.new_password.data)

        if 'profile_image' in request.files and request.files['profile_image'].filename:
            img_path = save_uploaded_image(request.files['profile_image'], folder_name='profiles')
            if img_path:
                current_user.profile_image = img_path

        current_user.full_name = form.full_name.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.index'))

    return render_template('profile/index.html', form=form)
