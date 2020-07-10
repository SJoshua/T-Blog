from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_login import login_user, login_required, logout_user, current_user
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
    View('Search','.search_article'),
    Subgroup(
        'Admin',
        View('New Article', '.new_article'),
        View('Manage Articles', '.manage_articles'),
        View('New Tag','.new_tag'),
        View('Manage Tags','.manage_tags'),
        View('New Category','.new_category'),
        View('Manage Categories','.manage_categories'),
        Separator(),
        View('Site Settings', '.site_settings'),
    ),
))



@frontend.route('/', methods=('GET', 'POST'))
def index():
    articles = get_articles()
    categories = get_categories()
    arr = []
    articles_arr = []
    categories_arr = []
    form = NewSearchForm()

    if form.validate_on_submit():
        
        return redirect('/result/?s=' + form.key_word.data + '&category=' + form.category.data.name + '&tag=' + form.tag.data.name)

    for i in range(min(len(articles),2)):
        arr.append((articles[i].id,articles[i].title))

    for i in range(len(articles)):
        user = get_user(articles[i].author)
        articles_arr.append((articles[i].id, articles[i].title,user.username,articles[i].date,articles[i].content))

    for i in range(len(categories)):
        articles = get_category_articles(categories[i].id)
        categories_arr.append((len(articles),categories[i].name))

    return render_template(get_current_theme().value + '/index.html', articles=articles_arr, show_articles = arr, categories=categories_arr, form = form)

@frontend.route('/article/<int:article_id>', methods=('GET', 'POST'))
def show_article(article_id):
    article = get_article(article_id)
    comments = get_comments(article_id)
    tags= get_article_tags(article_id)

    if not article:
        return render_template(get_current_theme().value + '/404.html')

    form = NewCommentForm()

    comments_arr = []
    for i in range(len(comments)):
        comments_arr.append((comments[i].id, comments[i].author, markdown(comments[i].content), comments[i].date))

    tags_arr = []
    for i in range(len(tags)):
        tag = get_tag(tags[i].tag_id)
        tags_arr.append((tag.id,tag.name))

    if form.validate_on_submit():
        # WARNING: UNSAFE!
        # TODO: Add filter for content
        insert_comment(article_id=article_id, author=form.author.data, email=form.email.data, content=form.content.data, ip=request.remote_addr, approved=True)
        return render_template(get_current_theme().value + '/article.html', title=article.title, content=markdown(article.content), author=get_user(article.author).nickname, category=get_category(article.category).name, date=article.date,comments=comments_arr,tags=tags_arr,form=form)

    return render_template(get_current_theme().value + '/article.html', title=article.title, content=markdown(article.content), author=get_user(article.author).nickname, category=get_category(article.category).name, date=article.date,comments=comments_arr,tags=tags_arr,form=form)

@frontend.route('/search', methods=('GET', 'POST'))
def search_article():
    form = NewSearchForm()

    if form.validate_on_submit():

       return redirect('/result/?s=' + form.key_word.data + '&category=' + form.category.data.name + '&tag=' + form.tag.data.name)
    
    return render_template(get_current_theme().value + '/search.html',form=form)

@frontend.route('/result/', methods=('GET', 'POST'))
def search_result():
    key_word = request.args.get('s', '', type=str)
    category_name = request.args.get('category', '', type=str)
    tag_name = request.args.get('tag', '', type=str)
    category_id = 0
    tag_id = 0
    form = NewSearchForm()
    articles = get_articles()
    categories = get_categories()
    arr = []
    sarr = []
    categories_arr = []

    for i in range(min(len(articles),2)):
        sarr.append((articles[i].id,articles[i].title))
    
    for i in range(len(categories)):
        articles = get_category_articles(categories[i].id)
        categories_arr.append((len(articles),categories[i].name))

    if category_name != '':
        category = search_category(category_name)
        if not category:
            category_id = -1
        else:
            category_id = category.id

    if tag_name != '':
        tag = search_tag(tag_name)
        if not tag:
            tag_id = -1
        else:
            tag_id = tag.id

    if key_word == '':
        articles = get_articles()
        for i in range(len(articles)):
            relation = get_relation(articles[i].id,tag_id)
            if tag_id == 0 or relation:
                if category_id == 0 or category_id == articles[i].category:
                    user = get_user(articles[i].author)
                    arr.append((articles[i].id, articles[i].title,user.username,articles[i].date,articles[i].content))
    else:
        articles = search_articles(key_word)
        for i in range(len(articles)):
            relation = get_relation(articles[i].id,tag_id)
            if tag_id == 0 or relation:
                if category_id == 0 or category_id == articles[i].category:
                    user = get_user(articles[i].author)
                    arr.append((articles[i].id, articles[i].title,user.username,articles[i].date,articles[i].content))

    return render_template(get_current_theme().value + '/index.html', articles = arr, show_articles = sarr, categories=categories_arr, form = form)

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
            return redirect(request.args.get('next') or url_for('frontend.index'))
        else:
            flash(u'Username or password is incorrect, please try again.', 'danger')
    if form.errors:
        flash(u'Failed. Please try again.', 'danger')

    return render_template(get_current_theme().value + '/login.html', form=form)

@frontend.route('/admin/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    nickname=form.nickname.data)
        db_session.add(user)
        db_session.commit()
        flash('Registration Succeed!')
        return redirect(url_for('frontend.login'))
    return render_template(get_current_theme().value + '/register.html', form=form)


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
        article_id = insert_article(title=form.title.data, content=form.content.data, author=current_user.id, category=form.category.data.id)
        for i in range(len(form.tag.data)):
            insert_tag_relation(article_id=article_id,tag_id=form.tag.data[i].id)
        return redirect(url_for('.index'))

    return render_template(get_current_theme().value + '/new_article.html', form=form)

@frontend.route('/admin/manage_articles', methods=('GET', 'POST'))
@login_required
def manage_articles():
    articles = get_articles()
    arr = []
    for i in range(len(articles)):
        arr.append((articles[i].id, articles[i].title))
    return render_template(get_current_theme().value + '/manage_articles.html', articles=arr)

@frontend.route('/admin/edit_article/<int:article_id>', methods=('GET', 'POST'))
@login_required
def edit_article(article_id):
    article = get_article(article_id)

    if not article:
        return render_template(get_current_theme().value + '/404.html')

    arr = []
    tags = get_article_tags(article_id)
    for i in range(len(tags)):
        tag = get_tag(tags[i].tag_id)
        arr.append(tag)
    form = NewArticleForm(category=get_category(article.category),tag=arr)

    if form.validate_on_submit():
        update_article(article_id=article_id, title=form.title.data, content=form.content.data, category=form.category.data.id)
        drop_tag_relation(article_id)
        for i in range(len(form.tag.data)):
            insert_tag_relation(article_id,form.tag.data[i].id)
        return redirect(url_for('.index'))

    form.title.data = article.title
    form.content.data = article.content

    return render_template(get_current_theme().value + '/edit_article.html', form=form)

@frontend.route('/admin/delete_article/<int:article_id>', methods=('GET', 'POST'))
@login_required
def delete_article(article_id):
    # TODO: Add confirmation? (Frontend)
    article = get_article(article_id)

    if not article:
        return render_template(get_current_theme().value + '/404.html')
    
    drop_article(article_id)

    return redirect(url_for('.index'))

@frontend.route('/admin/manage_comments/<int:article_id>', methods=('GET', 'POST'))
@login_required
def manage_comments(article_id):
    comments = get_comments(article_id)
    arr = []
    for i in range(len(comments)):
        arr.append((comments[i].id, comments[i].author,comments[i].email, markdown(comments[i].content), comments[i].date,comments[i].ip,comments[i].approved))
    return render_template(get_current_theme().value + '/manage_comments.html', comments=arr)

@frontend.route('/admin/edit_comment/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def edit_comment(comment_id):
    comment = get_comment(comment_id)
    
    if not comment:
        return render_template(get_current_theme().value + '/404.html')
    
    form = NewCommentForm()
    
    if form.validate_on_submit():
        update_comment(comment_id=comment_id,author=form.author.data,content=form.content.data)

        return redirect(url_for('.index'))
    
    form.author.data=comment.author
    form.content.data=comment.content

    return render_template('edit_comment.html',form=form)

@frontend.route('/admin/delete_comment/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def delete_comment(comment_id):
    # TODO: Add confirmation? (Frontend)
    comment = get_comment(comment_id)

    if not comment:
        return render_template(get_current_theme().value + '/404.html')
    
    drop_comment(comment_id)

    return redirect(url_for('.index'))

@frontend.route('/admin/site_settings', methods=('GET', 'POST'))
@login_required
def site_settings():
    form = NewSettingForm(theme=get_current_theme().value,address=get_site_url().value)

    if form.validate_on_submit():
        set_current_theme(form.theme.data)
        set_site_url(form.address.data)
        
        return redirect(url_for('.index'))

    return render_template(get_current_theme().value + '/setting.html',form=form)

@frontend.route('/admin/new_tag', methods=('GET', 'POST'))
@login_required
def new_tag():
    form = NewTagForm()

    if form.validate_on_submit():
        insert_tag(name=form.name.data)
        
        return redirect(url_for('.index'))

    return render_template(get_current_theme().value + '/new_tag.html', form=form)

@frontend.route('/admin/manage_tags', methods=('GET', 'POST'))
@login_required
def manage_tags():
    tags = get_tags()
    arr = []
    for i in range(len(tags)):
        arr.append((tags[i].id, tags[i].name))
    return render_template(get_current_theme().value + '/manage_tags.html', tags=arr)

@frontend.route('/admin/edit_tag/<int:tag_id>', methods=('GET', 'POST'))
@login_required
def edit_tag(tag_id):
    tag = get_tag(tag_id)

    if not tag:
        return render_template(get_current_theme().value + '/404.html')

    form = NewTagForm()

    if form.validate_on_submit():
        update_tag(tag_id=tag_id, name=form.name.data)
        
        return redirect(url_for('.index'))

    form.name.data=tag.name

    return render_template(get_current_theme().value + '/edit_tag.html', form=form)

@frontend.route('/admin/delete_tag/<int:tag_id>', methods=('GET', 'POST'))
@login_required
def delete_tag(tag_id):
    # TODO: Add confirmation? (Frontend)
    tag = get_tag(tag_id)

    if not tag:
        return render_template(get_current_theme().value + '/404.html')
    
    drop_tag(tag_id)

    return redirect(url_for('.index'))

@frontend.route('/admin/new_category', methods=('GET', 'POST'))
@login_required
def new_category():
    form = NewCategoryForm()

    if form.validate_on_submit():
        insert_category(name=form.name.data)
        
        return redirect(url_for('.index'))

    return render_template(get_current_theme().value + '/new_category.html', form=form)

@frontend.route('/admin/manage_categories', methods=('GET', 'POST'))
@login_required
def manage_categories():
    categories = get_categories()
    arr = []
    for i in range(len(categories)):
        if categories[i].name != 'Uncategorized':
            arr.append((categories[i].id, categories[i].name))
    return render_template(get_current_theme().value + '/manage_categories.html', categories=arr)

@frontend.route('/admin/edit_category/<int:category_id>', methods=('GET', 'POST'))
@login_required
def edit_category(category_id):
    category = get_category(category_id)

    if not category:
        return render_template(get_current_theme().value + '/404.html')

    form = NewCategoryForm()

    if form.validate_on_submit():
        update_category(category_id=category_id, name=form.name.data)
        
        return redirect(url_for('.index'))

    form.name=category.name

    return render_template(get_current_theme().value + '/edit_category.html', form=form)

@frontend.route('/admin/delete_category/<int:category_id>', methods=('GET', 'POST'))
@login_required
def delete_category(category_id):
    # TODO: Add confirmation? (Frontend)
    category = get_category(category_id)

    if not category:
        return render_template(get_current_theme().value + '/404.html')
    
    drop_category(category_id)

    return redirect(url_for('.index'))
