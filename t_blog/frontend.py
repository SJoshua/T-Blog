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

from .database import init_db
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
    return render_template('index.html')

@frontend.route('/article/<int:article_id>')
def show_article(article_id):
    return render_template('article.html', article_id = article_id)

@frontend.route('/init_db')
def init_database():
    init_db()
    return 'Done.'

@frontend.route('/admin/new_article', methods=('GET', 'POST'))
def new_article():
    form = NewArticleForm()

    if form.validate_on_submit():
        flash('Good Work!')

        return redirect(url_for('.index'))

    return render_template('new_article.html', form=form)
