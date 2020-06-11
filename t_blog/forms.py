from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import Required


class NewArticleForm(Form):
    title = TextField(u'Title', validators=[Required()])
    article = TextAreaField()
    
    submit = SubmitField(u'Publish')
