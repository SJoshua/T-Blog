from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *
from .database import db_session, User

class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(), Length(1, 60)])
    password = PasswordField(u'Password', validators=[DataRequired()])
    submit = SubmitField(u'Login')

class RegistrationForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(), Length(1, 60)])
    password = PasswordField(u'Password', validators=[DataRequired()])
    password2 = PasswordField(u'Confirm Password', validators=[DataRequired()])
    nickname = StringField(u'Nickname', validators=[DataRequired(), Length(1, 60)])
    email = StringField(u'Email', validators=[DataRequired(), Length(1, 60), Email()])
    submit = SubmitField(u'Submit')

    def validate_email(self, field):
        if db_session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if db_session.query(User).filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class NewArticleForm(FlaskForm):
    title = StringField(u'Title', validators=[Required()])
    content = TextAreaField(u'Article', render_kw={"rows": 20})
    submit = SubmitField(u'Publish')

class NewCommentForm(FlaskForm):
    author = StringField(u'Nickname', validators=[Required()])
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    content = TextAreaField(u'Comment', render_kw={"rows":5}, validators=[Required()])
    submit = SubmitField(u'Submit')

class NewTagForm(FlaskForm):
    name = StringField(u'name', validators=[Required()])
    submit = SubmitField(u'Submit')

class NewCategoryForm(FlaskForm):
    name = StringField(u'name', validators=[Required()])
    submit = SubmitField(u'Submit')