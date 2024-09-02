from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db,cache
from app.models.post import Post

bp = Blueprint('post', __name__)

@bp.route('/')
@bp.route('/posts')
@cache.cached(timeout=60)
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', posts=posts)

@bp.route('/post/<int:id>')
@cache.cached(timeout=300)
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('post.index'))
    return render_template('create_post.html')

@bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('post.post', id=id))
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post.post', id=id))
    return render_template('edit_post.html', post=post)

@bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('post.post', id=id))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('post.index'))