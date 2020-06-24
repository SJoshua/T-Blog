from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *

class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(), Length(1, 60)])
    password = PasswordField(u'Password', validators=[DataRequired()])
    submit = SubmitField(u'Login')

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