from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *
from .database import db_session, User, Category, Tag
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

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
    
    def query_category_factory():
        return [(r.id,r.name) for r in db_session.query(Category).all()]

    def get_category_pk(Obj):
        return Obj[1]
    
    category = QuerySelectField(u'Category', validators=[Required()], query_factory=query_category_factory, get_pk=get_category_pk)
    
    def query_tag_factory():
        return [(r.id,r.name) for r in db_session.query(Tag).all()]

    def get_tag_pk(Obj):
        return Obj[1]
    
    tag = QuerySelectMultipleField(u'Tag', validators=[Required()], query_factory=query_tag_factory, get_pk=get_tag_pk)
    
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
