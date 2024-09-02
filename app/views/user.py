# /app/views/user.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.forms.user_form import UserForm  # UserForm을 import 합니다. 이 폼을 먼저 생성해야 합니다.

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('user.profile'))
    return render_template('profile.html', form=form, user=current_user)

@bp.route('/user/delete', methods=['POST'])
@login_required
def delete_user():
    db.session.delete(current_user)
    db.session.commit()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('main.index'))