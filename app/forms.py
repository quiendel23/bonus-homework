from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class CityForm(FlaskForm):
    min_population = IntegerField('Min Population', validators=[DataRequired()])
    max_population = IntegerField('Max Population', validators=[DataRequired()])
    submit = SubmitField('Search for Cities')

class AddForm(FlaskForm):
    user_id = IntegerField('User ID:', validators=[DataRequired()])
    fname = StringField('First Name: ', validators=[DataRequired()])
    lname = StringField('Last Name:', validators=[DataRequired()])
    admin = StringField('Admin?: ', validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = StringField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Save')

class DeleteForm(FlaskForm):
    username = StringField('Username of User (Not you):', validators=[DataRequired()])
    submit = SubmitField('Delete')

class EvaluationForm(FlaskForm):
    user_id = IntegerField('User ID:', validators=[DataRequired()])
    fname = StringField('First Name: ', validators=[DataRequired()])
    lname = StringField('Last Name:', validators=[DataRequired()])