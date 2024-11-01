from app import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators= [DataRequired(), Length(min=6, max=20)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators= [DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField("Confirm Password", validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

class UpdateAccountForm(FlaskForm):
    pic = FileField("Profile Pic", validators=[FileAllowed('jpg', 'png')])
    submit= SubmitField("Upload image")
