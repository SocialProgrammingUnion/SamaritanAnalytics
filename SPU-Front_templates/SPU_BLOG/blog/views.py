from flask_blog import app
from flask_blog.settings import POSTS_PER_PAGE
from flask import render_template, redirect, flash, url_for, session, abort, request
from blog.form import SetupForm, PostForm
from flask_blog import db, uploaded_images
from user.models import User
from blog.models import Blog, Post, Category
from user.decorators import login_required, author_required
import bcrypt
from slugify import slugify

@app.route('/')

@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    blog = Blog.query.first()
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html', blog=blog, posts=posts)

@app.route('/admin')
@app.route('/index/<int:page>')
@login_required
@author_required
def admin(page=1):
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/admin.html', posts=posts)

@app.route('/setup', methods=('GET', 'POST'))
def setup():
    blogs = Blog.query.count()
    if blogs:
        return redirect(url_for('admin'))
    form = SetupForm()
    error = None
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        user = User(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            True
        )
        db.session.add(user)
        db.session.flush()
        if user.id:
            blog = Blog(form.name.data, user.id)
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = "Error creating user"
        if user.id and blog.id :
            db.session.commit()
            flash('Blog created')
            return redirect(url_for('index'))
        else:
            db.session.rollback()
            error = "Error creating blog"

        return redirect(url_for('admin'))
    return render_template('blog/setup.html', form=form, error=error)

@app.route('/post', methods=('GET','POST'))
@author_required
def post():
    form = PostForm()
    image = request.files.get('image')
    filename = None
    try:
        filename = uploaded_images.save(image)
    except:
        flash("The image was not uploaded")
    if form.validate_on_submit():
        flash('Forms Validated')
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data
        blog = Blog.query.first()
        author = User.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        post = Post(blog, author, title, body, category, slug, filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin'))
    else:
        flash('Forms did Not Validate')
    return render_template('blog/post.html', form=form, action='new')

@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
@author_required
def edit(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)
    if form.validate_on_submit():
        original_image = post.image
        form.populate_obj(post)
        if form.image.has_file():
            #import pdb; pdb.set_trace()
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded!")
            if filename:
                post.image = filename
        else:
            post.image = original_image
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category
        db.session.commit()
        return redirect(url_for('article', slug=post.slug))
    return render_template('blog/post.html', form=form, post=post, action="edit")

@app.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm(obj=post)
    #flash(post.id)
    return render_template('blog/article.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article Deleted")
    return redirect(url_for('admin'))