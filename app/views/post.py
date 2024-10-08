# /app/views/post.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.post import Post
from app.models.tag import Tag
from app.forms.post_form import PostForm
from app.forms.comment_form import CommentForm
from sqlalchemy.exc import SQLAlchemyError
from markdown2 import Markdown

markdowner = Markdown()

bp = Blueprint('post', __name__)

@bp.route('/')
@bp.route('/posts')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    print(posts.total)
    return render_template('index.html', posts=posts)

@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    post.content = markdowner.convert(post.content)
    form = CommentForm()
    return render_template('post.html', post=post, form=form)

@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)

            tag_names = [Tag.clean_tag_name(tag) for tag in form.tags.data.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                post.tags.append(tag)

            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('post.index'))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating post: {str(e)}")
            flash('An error occurred while creating your post. Please try again.', 'danger')
    return render_template('create_post.html', form=form)

@bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('post.post', id=id))

    form = PostForm()
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.content = form.content.data

            new_tag_names = [Tag.clean_tag_name(tag) for tag in form.tags.data.split(',') if tag.strip()]
            post.tags = [tag for tag in post.tags if tag.name in new_tag_names]

            for tag_name in new_tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                if tag not in post.tags:
                    post.tags.append(tag)

            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('post.post', id=id))
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating post: {str(e)}")
            flash('An error occurred while updating your post. Please try again.', 'danger')
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = ', '.join([tag.name for tag in post.tags])

    return render_template('edit_post.html', form=form, post=post)

@bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('post.post', id=id))
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting post: {str(e)}")
        flash('An error occurred while deleting your post. Please try again.', 'danger')
    return redirect(url_for('post.index'))

@bp.route('/api/search_tags')
def search_tags():
    query = request.args.get('q', '')
    current_app.logger.info(f"Searching tags with query: {query}")
    tags = Tag.query.filter(Tag.name.like(f'%{query}%')).all()
    return jsonify([{'id': tag.id, 'name': tag.name} for tag in tags])