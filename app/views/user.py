from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User

bp = Blueprint('user', __name__)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    current_user.username = request.form['username']
    current_user.email = request.form['email']
    db.session.commit()
    flash('Your profile has been updated.', 'success')
    return redirect(url_for('user.profile'))

@bp.route('/user/delete', methods=['POST'])
@login_required
def delete_user():
    db.session.delete(current_user)
    db.session.commit()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('main.index'))