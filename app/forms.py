"""
    Define forms used in app

"""

from flask.ext.wtf import Form
from wtforms.fields.html5 import URLField
from wtforms import StringField, DateField, SelectField, BooleanField, \
                    TextAreaField
from wtforms.validators import InputRequired, Optional, URL

# Same fields used to create and edit, so on a refactor cut down to just edit
class EditTodoForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    start_date = DateField('Started On', validators=[Optional()])
    due_date = DateField('Due On', validators=[Optional()])
    image = URLField('Image', validators=[Optional(), URL()])
    completed = BooleanField('Completed')
