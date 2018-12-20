# project/selections/forms.py

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class SelectionForm(Form):
	selection = StringField(
		'selection',
		validators=[DataRequired()]
		)
