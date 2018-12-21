# project/selections/forms.py

from flask_wtf import Form
from wtforms import SelectField
from wtforms.validators import DataRequired

class SelectionForm(Form):
	selection = RadioField('Label')
