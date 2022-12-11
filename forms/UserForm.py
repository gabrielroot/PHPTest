from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length

class UserCreate(Form):
  id = HiddenField()
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired(), Length(min=3, max=8)])
  name = StringField('name')
  email = StringField('email')