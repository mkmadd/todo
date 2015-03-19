from flask import render_template, flash, redirect
from app import app
from app.models import Project
from .forms import NewProjectForm

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        flash('New project creation requested for {}'.format(form.name.data))
        return redirect('/')
    return render_template('new_project.html', 
                            title='Create new project', 
                            form=form)
