#!/usr/bin/python3
"""Module describes form classes."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
# from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class LoginForm(FlaskForm):
    """A form class for login.

    Attributes:
        token (str): String token used to validate deriv accounts
    """

    token = PasswordField(label='Deriv Token', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')
