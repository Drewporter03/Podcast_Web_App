from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from functools import wraps
import podcast.authentication.services as services
import podcast.adapters.repository as repo
import podcast.episodes.services

import podcast.playlists.services as playlist_services

authentication_bp = Blueprint(
    'authentication_bp', __name__, template_folder='templates')


@authentication_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    error_msg = None
    password_error = None
    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repository)
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            error_msg = 'Username is not unique'

    return render_template(
        'main.html',
        content_right='authentication.html',
        title='Welcome to mixcast.',
        form=form,
        return_error_msg=error_msg,
        unknown_password_error=password_error,
        handler_url=url_for('authentication_bp.register'),
    )


@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_msg = None
    password_error = None
    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repository)
            services.authenticate_user(user.username, form.password.data, repo.repository)
            session.clear()
            session['user_name'] = user.username
            user_name = session.get('user_name')
            playlist_services.add_playlist(repo.repository, user_name, f"{user_name}'s playlist")
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            error_msg = 'User not found'
        except services.AuthenticationException:
            password_error = 'Invalid username or password'
    return render_template(
        'main.html',
        content_right='authentication.html',
        return_error_msg=error_msg,
        unknown_password_error=password_error,
        title='Welcome back.',
        form=form,
    )


@authentication_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)

    return wrapped_view


def password_validator(form, field):
    password = field.data
    upper_check = False
    lower_check = False
    digit_check = False

    for char in password:
        if char.isdigit():
            digit_check = True
        elif char.isupper():
            upper_check = True
        elif char.islower():
            lower_check = True

    if upper_check is False:
        raise ValidationError(
            "Password must contain at least one upper case letter, one lower case and at least one digit.")
    if lower_check is False:
        raise ValidationError(
            "Password must contain at least one upper case letter, one lower case and at least one digit.")
    if digit_check is False:
        raise ValidationError(
            "Password must contain at least one upper case letter, one lower case and at least one digit.")


def user_validator(form, field):
    username = field.data
    if ' ' in username:
        raise ValidationError("Username cannot contain spaces")


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Username cannot be empty'),
        Length(min=3, message='Username must be at least 3 characters long'), user_validator],
                            render_kw={"class": 'test'})
    password = PasswordField('Password', [
        DataRequired(message='Password cannot be empty'),
        Length(min=6, message='Password must be at least 6 characters long'),
        password_validator], render_kw={"class": 'test'})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Username cannot be empty')], render_kw={"class": 'test'})
    password = PasswordField('Password', [
        DataRequired(message='Password cannot be empty')], render_kw={"class": 'test'})
    submit = SubmitField('Log in')


