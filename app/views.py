from flask import render_template, flash, redirect
from app import app
from .forms import NewProjectForm

@app.route('/')
def index():
    project = {'name': 'Project 3'}
    return render_template('index.html', project=project)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        flash('New project creation requested for {}'.format(form.name.data))
        return redirect('/')
    return render_template('new_project.html', 
                            title='Create new project', 
                            form=form)
