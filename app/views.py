from flask import render_template, flash, redirect, url_for, session, abort, \
                  request
from app import app, db, lm
from .models import User, Todo
from .forms import NewTodoForm, EditTodoForm
from bleach import clean
from flask.ext.login import login_user, logout_user, current_user, \
                            login_required
from oauth import OAuthSignIn

@app.route('/')
def index():
    # TODO: leave as is or break out into separate login page?
    if current_user.is_authenticated():
        projects = Todo.query.filter_by(parent_id=None, owner=current_user).all()
    else:
        projects = None
    return render_template('index.html', projects=projects)

@app.route('/todos/new', methods=['GET', 'POST'])
@app.route('/todos/<int:id>/new', methods=['GET', 'POST'])
@login_required
def new_todo(id=None):
    if id is None:
        parent = None
    else:
        parent = Todo.query.get(id)
        if parent is None:
            flash('Todo id {} not found.'.format(id))
            return redirect(url_for('index'))
        if parent.owner != current_user:
            flash('You are not authorized to edit that todo item')
            return redirect(url_for('index'))
    form = NewTodoForm()
    #form.project_id.choices = [(p.id, p.name) for p in Todo.query.order_by('name')]
    if form.validate_on_submit():
        #parent_project = Todo.query.get(form.project_id.data)
        new_todo = Todo(form.name.data, current_user, parent)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo {} created.'.format(new_todo.name))
        if parent is None:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('show_todo', id=parent.id))
    title = 'Create new {}'.format('project' if parent is None else 'todo')
    return render_template('new_todo.html', title=title, form=form)

@app.route('/todos/<int:id>')
@login_required
def show_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id))
        return redirect(url_for('index'))
    if todo.owner != current_user:
        flash('You are not authorized to view that todo item')
        return redirect(url_for('index'))
    return render_template('todo.html', title=todo.name, todo=todo)

@app.route('/todos/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id))
        return redirect(url_for('index'))
    if todo.owner != current_user:
        flash('You are not authorized to edit that todo item')
        return redirect(url_for('index'))
    form = EditTodoForm(obj=todo)
    if form.validate_on_submit():
        # Allow html in description like links, but remove dangerous tags
        form.description.data = clean(form.description.data)  # sanitize
        form.populate_obj(todo)
        db.session.commit()
        flash('Todo <{}> updated.'.format(todo.name))
        return redirect(url_for('show_todo', id=id))
    return render_template('edit_todo.html', title=todo.name, form=form)

@app.route('/todos/<int:id>/delete', methods=['POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id))
        return redirect(url_for('index'))
    if todo.owner != current_user:
        flash('You are not authorized to delete that todo item')
        return redirect(url_for('index'))
    db.session.delete(todo)
    db.session.commit()
    flash('Todo id {0} ({1}) deleted.'.format(id, todo.name))
    return redirect(url_for('index'))

# from Miguel Grinberg's https://github.com/miguelgrinberg/flask-oauth-example
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# from Miguel Grinberg's https://github.com/miguelgrinberg/flask-oauth-example
@app.route('/logout')
@login_required
def logout():
    provider = session.pop('provider')
    oauth = OAuthSignIn.get_provider(provider)
    status_code = oauth.revoke(session.pop('access_token'))
    if status_code not in [200, 204]:
        flash('Failed to revoke access token!'
              '  Status code: {}'.format(status_code))
    logout_user()
    flash('Logged out.')
    return redirect(url_for('index'))

# from Miguel Grinberg's https://github.com/miguelgrinberg/flask-oauth-example
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # print '\nStep 1.  User tries to log in.\n'
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

# modified from Miguel Grinberg's
# https://github.com/miguelgrinberg/flask-oauth-example
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    # print '\nStep 3.  Oauth provider ({}) makes callback.\n'.format(provider)
    social_id, name, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        # user = User(social_id=social_id, nickname=username, email=email)
        user = User(social_id=social_id)
        user.name = name
        user.email = email
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    session['provider'] = provider
    flash('Logged in successfully.')
    # TODO: handle next or get rid of it?
    next = request.args.get('next')
    print '\nThe value of next is: {}\n'.format(next)
    return redirect(url_for('index'))
