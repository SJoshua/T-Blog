from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *

class NewArticleForm(FlaskForm):
    title = TextField(u'Title', validators=[Required()])
    content = TextAreaField(u'Article', render_kw={"rows": 20})
    submit = SubmitField(u'Publish')
