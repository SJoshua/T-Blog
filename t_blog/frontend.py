from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_login import login_user, login_required, logout_user
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape
from markdown import markdown

from .database import *
from .forms import *
from .nav import nav

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('T-Blog', '.index'),
    View('Home', '.index'),
    Subgroup(
        'Admin',
        View('New Article', '.new_article'),
        View('Manage Articles', '.manage_articles'),
        View('Site Settings', '.site_settings'),
    ),
))

@frontend.route('/')
def index():
    articles = get_articles()
    arr = []
    for i in range(len(articles)):
        arr.append((articles[i].id, articles[i].title))
    return render_template('index.html', articles=arr)

@frontend.route('/article/<int:article_id>', methods=('GET', 'POST'))
def show_article(article_id):
    article = get_article(article_id)
    comments = get_comment(article_id)

    if not article:
        return render_template('404.html')

    form = NewCommentForm()

    if form.validate_on_submit():
        # WARNING: UNSAFE!
        # TODO: Add filter for content
        insert_comment(article_id=article_id, author=form.author.data, email=form.email.data, content=form.content.data, ip=request.remote_addr, approved=True)

    arr = []
    for i in range(len(comments)):
        arr.append((comments[i].id, comments[i].author, markdown(comments[i].content), comments[i].date))

    return render_template('article.html', title=article.title, content=markdown(article.content), author=get_author_name(article.author), category=get_category_name(article.category), comments=arr, form=form)

# for development
@frontend.route('/init_db')
def init_database():
    init_db()
    return 'Done.'

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = verify_password(username=form.username.data, password=form.password.data)
        if user:
            login_user(user)
            flash(u'Welcome back, %s!' % user.nickname, 'success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash(u'Username or password is incorrect, please try again.', 'danger')
    if form.errors:
        flash(u'Failed. Please try again.', 'danger')

    return render_template('login.html', form=form)

@frontend.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'You are now logged out.', 'success')
    return redirect(url_for('.index'))

@frontend.route('/admin/new_article', methods=('GET', 'POST'))
@login_required
def new_article():
    form = NewArticleForm()

    if form.validate_on_submit():
        insert_article(title=form.title.data, content=form.content.data, author=1, category=1)
        
        return redirect(url_for('.index'))

    return render_template('new_article.html', form=form)

@frontend.route('/admin/manage_articles', methods=('GET', 'POST'))
@login_required
def manage_articles():
    articles = get_articles()
    arr = []
    for i in range(len(articles)):
        arr.append((articles[i].id, articles[i].title))
    return render_template('manage_articles.html', articles=arr)

@frontend.route('/admin/edit_article/<int:article_id>', methods=('GET', 'POST'))
@login_required
def edit_article(article_id):
    article = get_article(article_id)

    if not article:
        return render_template('404.html')

    form = NewArticleForm()

    if form.validate_on_submit():
        update_article(article_id=article_id, title=form.title.data, content=form.content.data, category=1)
        
        return redirect(url_for('.index'))

    form.title.data = article.title
    form.content.data = article.content

    return render_template('edit_article.html', form=form)

@frontend.route('/admin/delete_article/<int:article_id>', methods=('GET', 'POST'))
@login_required
def delete_article(article_id):
    # TODO: Add confirmation? (Frontend)
    article = get_article(article_id)

    if not article:
        return render_template('404.html')
    
    drop_article(article_id)

    return redirect(url_for('.index'))

@frontend.route('/admin/manage_comments/<int:article_id>', methods=('GET', 'POST'))
@login_required
def manage_comments():
    return "Building ..."

@frontend.route('/admin/site_settings', methods=('GET', 'POST'))
@login_required
def site_settings():
    return "Building ..."

