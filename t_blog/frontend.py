# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape
from markdown import markdown

from .database import *
from .forms import NewArticleForm
from .nav import nav

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('T-Blog', '.index'),
    View('Home', '.index'),
    View('Admin', '.new_article'), ))

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/')
def index():
    articles = get_articles()
    arr = []
    for i in range(len(articles)):
        arr.append((articles[i].id, articles[i].title))
    return render_template('index.html', articles=arr)

@frontend.route('/article/<int:article_id>')
def show_article(article_id):
    article = get_article(article_id)
    return render_template('article.html', title=article.title, content=markdown(article.content), author=get_author_name(article.author), category=get_category_name(article.category))

@frontend.route('/init_db')
def init_database():
    init_db()
    return 'Done.'

@frontend.route('/admin/new_article', methods=('GET', 'POST'))
def new_article():
    form = NewArticleForm()

    if form.validate_on_submit():
        insert_article(title=form.title.data, content=form.content.data, author=1, category=1)
        
        return redirect(url_for('.index'))

    return render_template('new_article.html', form=form)
