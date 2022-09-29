from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
#from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email
from movie.db_setup import Movies, User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username Already Existed, Please Try Different One .')
    
    def validate_email_address(self, email_address_to_check):
        email_address=User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address Already Existed, Please Try Different One .')

    username=StringField(label='Username', validators=[DataRequired(), Length(min=5, max=30)])
    email_address=StringField(label='Email Address', validators=[DataRequired(), Email()])
    password_1=PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=60)])
    password_2=PasswordField(label='Password Confirmation', validators=[DataRequired(), EqualTo('password_1')])
    submit=SubmitField(label='Submit')

class LoginForm(FlaskForm):
    username=StringField(label='Username')
    password=PasswordField(label='Password')
    submit=SubmitField(label='Submit')

class FetchMovie(FlaskForm):
    movie_title=StringField(label='Movie Title', validators=[DataRequired()])
    media_type=SelectField(label='Type', choices=[('movie', 'movie'), ('series', 'series')])
    submit=SubmitField(label='Post')

class CommentOnMovie(FlaskForm):
    comment_area=TextAreaField(label='Comment', validators=[Length(max=2000), DataRequired()])
    submit=SubmitField(label='Post')

class LikeMovie(FlaskForm):
    like=SubmitField(label='Like')