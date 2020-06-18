from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *

class NewArticleForm(FlaskForm):
    title = StringField(u'Title', validators=[Required()])
    content = TextAreaField(u'Article', render_kw={"rows": 20})
    submit = SubmitField(u'Publish')

class NewCommentForm(FlaskForm):
    author = StringField(u'Nickname', validators=[Required()])
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    content = TextAreaField(u'Comment', render_kw={"rows":5}, validators=[Required()])
    submit = SubmitField(u'Submit')