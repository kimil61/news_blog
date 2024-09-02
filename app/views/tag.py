from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required
from app import db
from app.models.tag import Tag
from app.models.post import Post

bp = Blueprint('tag', __name__)

@bp.route('/tags')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@bp.route('/tag/<string:tag_name>')
def tag_posts(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = tag.posts.order_by(Post.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('tag_posts.html', tag=tag, posts=posts)

@bp.route('/tag/create', methods=['POST'])
@login_required
def create_tag():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for('tag.tags'))

@bp.route('/tag/<int:tag_id>/delete', methods=['POST'])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tag.tags'))

@bp.route('/api/search_tags')
def search_tags():
    query = request.args.get('q', '')
    tags = Tag.query.filter(Tag.name.like(f'%{query}%')).all()
    return jsonify([{'id': tag.id, 'name': tag.name} for tag in tags])

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    tags = Tag.query.filter(Tag.name.like(f'%{query}%')).all()
    posts = Post.query.filter(Post.tags.any(Tag.name.in_([tag.name for tag in tags]))).all()
    return render_template('search_results.html', posts=posts, query=query)