from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *

class NewArticleForm(FlaskForm):
    title = StringField(u'Title', validators=[Required()])
    content = TextAreaField(u'Article', render_kw={"rows": 20})
    submit = SubmitField(u'Publish')

class NewCommentForm(FlaskForm):
    article_id = TextAreaField(u'Article_id',validators=[Required()])
    author = TextAreaField(u'Author',validators=[Required()])
    email = TextAreaField(u'Email',validators=[Required()])
    content = TextAreaField(u'Comment',render_kw={"rows":20})
    ip = TextAreaField(u'IP',validators=[Required()])
    submit = SubmitField(u'Publish')