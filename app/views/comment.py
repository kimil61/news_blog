# app/views/comment.py
from flask import Blueprint, redirect, url_for, flash, request, current_app, render_template
from flask_login import login_required, current_user
from app import db
from app.models.comment import Comment
from app.models.post import Post
from app.forms.comment_form import CommentForm
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('comment', __name__)

@bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def create_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        try:
            post = Post.query.get_or_404(post_id)
            comment = Comment(content=form.content.data, user=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating comment: {str(e)}")
            flash('An error occurred while posting your comment. Please try again.', 'danger')
    return redirect(url_for('post.post', id=post_id))

@bp.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user != current_user:
        flash('You can only edit your own comments.', 'danger')
        return redirect(url_for('post.post', id=comment.post.id))

    form = CommentForm()
    if form.validate_on_submit():
        try:
            comment.content = form.content.data
            db.session.commit()
            flash('Your comment has been updated!', 'success')
            return redirect(url_for('post.post', id=comment.post.id))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating comment: {str(e)}")
            flash('An error occurred while updating your comment. Please try again.', 'danger')
    elif request.method == 'GET':
        form.content.data = comment.content
    return render_template('edit_comment.html', form=form, comment=comment)


@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user != current_user:
        flash('You can only delete your own comments.', 'danger')
        return redirect(url_for('post.post', id=comment.post_id))

    post_id = comment.post_id  # 댓글 삭제 전에 post_id를 저장

    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Your comment has been deleted!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting comment: {str(e)}")
        flash('An error occurred while deleting your comment. Please try again.', 'danger')

    return redirect(url_for('post.post', id=post_id))