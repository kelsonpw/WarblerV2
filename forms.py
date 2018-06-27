from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    text = StringField('text', validators=[DataRequired()], widget=TextArea())


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    location = StringField('Location', validators=[Length(min=5, max=30)])
    bio = TextAreaField('Bio', validators=[Length(min=8, max=100)])
    header_image_url = StringField(
        '(Optional) Header Image URL', default="hidden")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
