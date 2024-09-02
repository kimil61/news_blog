from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class TagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Create Tag')