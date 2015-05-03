from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField
from wtforms import StringField, SelectField, DateTimeField, BooleanField, \
                    TextAreaField
from wtforms.validators import DataRequired, Optional, URL

class NewProjectForm(Form):
    name = StringField('Name', validators=[DataRequired()])

class NewTodoForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    #project_id = SelectField('Parent Project', coerce=int)

class EditProjectForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateTimeField('Started On', validators=[Optional()])
    due_date = DateTimeField('Due On', validators=[Optional()])
    completed = BooleanField('Completed')
    image = URLField('Image', validators=[Optional(), URL()])

class EditTodoForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    start_date = DateTimeField('Started On', validators=[Optional()])
    due_date = DateTimeField('Due On', validators=[Optional()])
    completed = BooleanField('Completed')
    image = URLField('Image', validators=[Optional(), URL()])
