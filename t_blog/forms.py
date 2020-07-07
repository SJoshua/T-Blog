from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *
from .database import db_session, User, Category, Tag, Setting
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

import os

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
        return [Category(r.id,r.name) for r in db_session.query(Category).all()]

    def query_tag_factory():
        return [Tag(r.id,r.name) for r in db_session.query(Tag).all()]
    
    def get_pk(Obj):
        return Obj.id
    
    def get_label(Obj):
        return Obj.name

    category = QuerySelectField(u'Category', validators=[Required()], query_factory=query_category_factory, get_pk=get_pk,get_label=get_label)
    tag = QuerySelectMultipleField(u'Tag', validators=[Optional()], query_factory=query_tag_factory, get_pk=get_pk,get_label=get_label)
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

class NewSearchForm(FlaskForm):
    category = StringField(u'Category',validators=[Optional()])
    tag = StringField(u'Tag',validators=[Optional()])
    key_word = StringField(u'Keywords',validators=[Optional()])
    search = SubmitField(u'Search')

class NewSettingForm(FlaskForm):
    def get_themes():
        it = os.walk('./t_blog/templates')
        themes = []
        for path, dir_list, file_list in it:
            for theme_name in dir_list:
                themes.append((theme_name, theme_name))
        return themes
    
    def get_pk(Obj):
        return Obj.id

    def get_label(Obj):
        return Obj.value

    # Theme = QuerySelectField(u'Theme',validators=[Required()],query_factory=query_factory,get_pk=get_pk,get_label=get_label)
    theme = SelectField(u'Theme', choices=get_themes())
    address = StringField(u'Address',validators=[Required()]) 
    submit = SubmitField(u'Submit')