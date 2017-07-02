# project/users/forms.py


from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])


class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])


class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])


class EditUserForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    user_role = RadioField('User Role', validators=[DataRequired()],
                           choices=[('user', 'User Role'),
                                    ('admin', 'Administrator Role')],
                           default='user')
    new_password = PasswordField('New Password', validators=[])
    new_confirm = PasswordField('Repeat New Password', validators=[EqualTo('new_password')])
    email_confirmed = BooleanField('Email Confirmed', default="")
