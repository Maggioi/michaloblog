from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, BooleanField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Submit")
