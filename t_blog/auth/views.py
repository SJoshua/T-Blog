from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User
from .forms import LoginForm
from ..database import db_session


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter_by(username=form.usr_name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash(u'登陆成功！欢迎回来，%s!' % user.username, 'success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆。', 'danger')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆。', 'success')
    return redirect(url_for('main.index'))