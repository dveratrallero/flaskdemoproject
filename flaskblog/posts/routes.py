from flask import Blueprint, render_template, request, url_for, abort, flash, redirect
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)

#POST ROUTES

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    page=request.args.get('page', 1, type=int)
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post=post)\
    .order_by(Comment.timestamp.desc())\
    .paginate(page= page, per_page=5)
    return render_template('post.html', title=post.title, post= post, comments=comments)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html', title="Update Post", form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    comments = Comment.query.filter_by(post=post)\
    .order_by(Comment.timestamp.desc())\
    .paginate(page= page, per_page=5)
    for comment in comments.items:
        db.session.delete(comment)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


#COMMENT ROUTES


@posts.route("/post/<int:post_id>/comment/<int:comment_id>")
def comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.filter_by(post=post, id=comment_id).first_or_404()
    return render_template('singlepagecomment.html', title=post.title, post= post, comment=comment)

@posts.route("/post/<int:post_id>/comment/new", methods=['GET', 'POST'])
@login_required
def new_post_comment(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, com_author=current_user, post=post)
        Comment.save(comment)
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post_comment.html', title='New comment', form=form, post=post)
