from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps
import podcast.authentication.services as services
import podcast.adapters.repository as repo


authentication_bp = Blueprint(
    'authentication_bp', __name__, template_folder='templates')

@authentication_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    error_msg = ""
    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repository)
            return redirect(url_for('authentication_bp.login'))
        except Exception as e:
            error_msg = "User name not unique"

    return render_template(
        'main.html',
        content_right='authentication.html',
        title='Register',
        form=form,
        return_error_msg = error_msg,
        handler_url=url_for('authentication_bp.register'),
    )


class PasswordValid:
    def __init__(self):
        None
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(6) \
            .max(100) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()

        if not schema.validate(field.data):
            raise ValidationError("Password must be at least 6 chars long, one uppercase letter and one lower case letter and one digit ")

        common_passwords = ['Password', 'passw0rd1',  'Password123']
        if field.data in common_passwords:
            raise ValidationError("Cannot use common passwords such as ['Password', 'password',  'Password123'] ")

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Username cannot be empty'),
        Length(min=3, message='Username must be at least 3 characters long'),])
    password = PasswordField('Password', [
        DataRequired(message='Password cannot be empty'),
        PasswordValid()])
    submit = SubmitField('complete')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Username cannot be empty')])
    password = PasswordField('Password', [
        DataRequired(message='Password cannot be empty')])
    submit = SubmitField('Login')