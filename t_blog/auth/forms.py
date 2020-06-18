from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    usr_name = StringField(u'用户名', validators=[DataRequired(), Length(1, 60)])
    password = PasswordField(u'密码', validators=[DataRequired()])