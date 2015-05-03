from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import User, Todo
from .forms import NewProjectForm, NewTodoForm, EditProjectForm, EditTodoForm
from bleach import clean

@app.route('/')
def index():
    projects = Todo.query.filter_by(parent_id=None).all()
    return render_template('index.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        new_project = Todo(form.name.data)
        db.session.add(new_project)
        db.session.commit()
        flash('Project {} created.'.format(new_project.name))
        return redirect(url_for('index'))
    return render_template('new_project.html', 
                            title='Create new project', 
                            form=form)


# TODO: get rid of unnecessary project vs todo
@app.route('/projects/<int:id>')
def show_project(id):
    project = Todo.query.get(id)
    if project is None or project.parent_id is not None:
        flash('Project id {} not found.'.format(id))
        return redirect(url_for('index'))
    return render_template('project.html', title=project.name, project=project)

@app.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    project = Todo.query.get(id)
    if project is None:
        flash('Project id {} does not exist.'.format(id))
        return redirect(url_for('index'))
    form = EditProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
        flash('Project <{}> updated.'.format(project.name))
        return redirect(url_for('show_project', id=project.id))
    return render_template('edit_project.html', title=project.name, form=form)

@app.route('/projects/<int:id>/delete', methods=['POST'])
def delete_project(id):
    project = Todo.query.get(id)
    if project is None:
        flash('Project id {} not found.'.format(id))
        return redirect(url_for('index'))
    db.session.delete(project)
    db.session.commit()
    flash('Project id {0} ({1}) deleted.'.format(id, project.name))
    return redirect(url_for('index'))

@app.route('/projects/<int:id>/todos/new', methods=['GET', 'POST'])
def new_todo(id):
    parent_project = Todo.query.get(id)
    if parent_project is None:
        flash('Project id {} not found.'.format(id))
        return redirect(url_for('index'))
    form = NewTodoForm()
    #form.project_id.choices = [(p.id, p.name) for p in Todo.query.order_by('name')]
    if form.validate_on_submit():
        #parent_project = Todo.query.get(form.project_id.data)
        new_todo = Todo(form.name.data, parent_project)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo {} created.'.format(new_todo.name))
        return redirect(url_for('show_project', id=parent_project.id))
    return render_template('new_todo.html', 
                            title='Create new todo', 
                            form=form)

@app.route('/todos/<int:id>')
def show_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id))
        return redirect(url_for('index'))
    return render_template('todo.html', title=todo.name, todo=todo)

@app.route('/todos/<int:id>/edit', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id))
        return redirect(url_for('index'))
    form = EditTodoForm(obj=todo)
    if form.validate_on_submit():
        form.description.data = clean(form.description.data)  # sanitize
        form.populate_obj(todo)
        db.session.commit()
        flash('Todo <{}> updated.'.format(todo.name))
        return redirect(url_for('show_todo', id=id))
    return render_template('edit_todo.html', title=todo.name, form=form)

@app.route('/todos/<int:id>/delete', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id))
        return redirect(url_for('index'))
    db.session.delete(todo)
    db.session.commit()
    flash('Todo id {0} ({1}) deleted.'.format(id, todo.name))
    return redirect(url_for('index'))
