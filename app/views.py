"""
    All routing functions for Much Todo About Nothing
    
"""

from flask import render_template, flash, redirect, url_for, session, abort, \
                  request, jsonify, make_response
from app import app, db, lm
from .models import User, Todo
from .forms import EditTodoForm
from flask.ext.login import login_user, logout_user, current_user, \
                            login_required
from bleach import clean            # for sanitizing user input
from oauth import OAuthSignIn
from dicttoxml import dicttoxml     # for XML output


# Main entry point.  If user is authenticated, show all user's projects
@app.route('/')
def index():
    if current_user.is_authenticated():
        projects = Todo.query.filter_by(parent_id=None, 
                                        owner=current_user).all()
    else:
        projects = None
    return render_template('index.html', projects=projects)


# Create a new todo or project.  A project is just a todo with no parent.
# If id is passed in, new todo is created as child of todo with that id
@app.route('/todos/new', methods=['GET', 'POST'])
@app.route('/todos/<int:id>/new', methods=['GET', 'POST'])
@login_required
def new_todo(id=None):
    if id is None:      # ...this is a project
        parent = None
        ancestry = []
    else:               # ...this is a child todo
        parent = Todo.query.get(id)
        
        # Check to make sure parent exists and is owned by current_user
        if not parent:
            flash('Todo id {} not found.'.format(id), 'warning')
            return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
        if parent.owner != current_user:
            flash('You are not authorized to edit that todo item', 'danger')
            return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
        ancestry = get_ancestry(parent)
        ancestry.append(parent)
        
    # Originally had a separate, simple form for new todos, but rereading the
    # rubric went to full edit fields
    form = EditTodoForm()
    
    if form.validate_on_submit():
        # Create new todo and save to database
        new_todo = Todo(form.name.data, current_user, parent)
        # Allow html in description like links, but remove dangerous tags
        form.description.data = clean(form.description.data)  # sanitize
        form.populate_obj(new_todo)
        db.session.add(new_todo)
        db.session.commit()
        
        flash('{0} <{1}> created.'.format('Todo' if parent else 'Project', 
                                          new_todo.name), 'success')
        
        # If todo with parent, return html to show new project's parent
        # (rest of data is just to mirror project return)
        if parent:
            if request.is_xhr:  # for AJAX request
                data = {
                    'html': render_template('todo.html', 
                                    todo=new_todo.parent,
                                    ancestry=get_ancestry(new_todo.parent)),
                    'name': new_todo.name,
                    'url': ("javascript:call_url('{}', 'GET')"
                            .format(url_for('show_todo', id=new_todo.id))),
                    'id' : new_todo.id,
                    'completed': new_todo.completed,
                    'is_project': False
                }
                return jsonify(data)
            else:               # for normal http request
                return redirect(url_for('show_todo', id=new_todo.id))
        # if project, return html to show new project and data to create side
        # nav pill.
        else:
            if request.is_xhr:  # for AJAX request
                data = {
                    'html': render_template('todo.html', 
                                    todo=new_todo, 
                                    ancestry=[]),
                    'name': new_todo.name,
                    'url': ("javascript:call_url('{}', 'GET')"
                            .format(url_for('show_todo', id=new_todo.id))),
                    'id' : new_todo.id,
                    'completed': new_todo.completed,
                    'is_project': True
                }
                return jsonify(data)
            else:               # for normal http request
                return redirect(url_for('show_todo', id=parent.id))
    return render_template('new_todo.html', parent=parent, form=form, 
                           ancestry=ancestry)


# Display todo with given id
@app.route('/todos/<int:id>')
@login_required
def show_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id), 'warning')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    if todo.owner != current_user:
        flash('You are not authorized to view that todo item', 'danger')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    return render_template('todo.html', todo=todo, ancestry=get_ancestry(todo))


# Edit todo with given id
@app.route('/todos/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id), 'warning')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    if todo.owner != current_user:
        flash('You are not authorized to edit that todo item', 'danger')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    form = EditTodoForm(obj=todo)
    if form.validate_on_submit():
        # Allow html in description (like links), but remove dangerous tags
        form.description.data = clean(form.description.data)  # sanitize
        form.populate_obj(todo)
        db.session.commit()
        flash('Todo <{}> updated.'.format(todo.name), 'success')
        # if AJAX request, return show html and data to update side nav pill
        if request.is_xhr:
            data = {
                'html': render_template('todo.html', 
                                        todo=todo, 
                                        ancestry=get_ancestry(todo)),
                'completed': todo.completed,
                'id': todo.id,
                'name': todo.name,
                'is_root': todo.parent is None
            }
            return jsonify(data)
        else:                   # else just show todo
            return redirect(url_for('show_todo', id=todo.id))
    return render_template('edit_todo.html', todo=todo, form=form, 
                           ancestry=get_ancestry(todo))


# delete todo with given id
@app.route('/todos/<int:id>/delete', methods=['POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id), 'warning')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    if todo.owner != current_user:
        flash('You are not authorized to delete that todo item', 'danger')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    parent = todo.parent
    db.session.delete(todo)
    db.session.commit()
    flash('Todo id {0} ({1}) deleted.'.format(id, todo.name), 'success')
    if request.is_xhr:      # if AJAX...
        if parent is None:  # ... and root, return data to remove side nav pill
            data = {
                'html': render_template('default.html'),    # show default page
                'delete': True,
                'id': todo.id
            }
        else:               # ... else just show parent page
            data = {
                'html': render_template('todo.html', 
                                todo=parent, 
                                ancestry=get_ancestry(parent)),
                'delete': False,
                'id': parent.id
            }
        return jsonify(data)
    else:
        return redirect(url_for('index'))


# toggle the boolean 'completed' attribute of todo with given id
@app.route('/todos/<int:id>/toggle_comp', methods=['POST'])
@login_required
def toggle_comp_todo(id):
    todo = Todo.query.get(id)
    if todo is None:
        flash('Todo id {} not found.'.format(id), 'warning')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    if todo.owner != current_user:
        flash('You are not authorized to edit that todo item', 'danger')
        return return_ajax_or_http(request.is_xhr, 'default.html', 'index')
    todo.completed = not todo.completed     # toggle value of completed
    db.session.commit()
    
    status = 'complete' if todo.completed else 'not complete'
    flash('Todo id {0} ({1}) marked {2}.'.format(id, todo.name, status),
          'success')
    # if AJAX request, return show html and data to update side nav pill
    if request.is_xhr:
        data = {
            'html': render_template('todo.html', 
                                    todo=todo, 
                                    ancestry=get_ancestry(todo)),
            'completed': todo.completed,
            'id': todo.id,
            'name': todo.name,
            'is_root': todo.parent is None
        }
        return jsonify(data)
    else:
        return redirect(url_for('show_todo', id=todo.id))


# Helper function to create breadcrumb trail; get all ancestors of this todo
def get_ancestry(todo):
    ancestry = []
    if todo is None:
        return ancestry
    parent = todo.parent
    while parent is not None:
        ancestry.insert(0, parent)
        parent = parent.parent
    return ancestry

# Helper function to try to DRY up some code
def return_ajax_or_http(is_ajax, ajax_template, http_template):
    if is_ajax:         # for AJAX request
        return render_template(ajax_template)
    else:               # for normal http request
        return redirect(url_for(http_template))


#### User Management Functions

# required function for LoginManager
# from Miguel Grinberg's https://github.com/miguelgrinberg/flask-oauth-example
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))  # id is unicode

# logout current_user, first revoking access token if possible
@app.route('/logout')
@login_required
def logout():
    if 'provider' in session:
        provider = session.pop('provider')
    else:
        flash("KeyError: 'provider' not in session", 'danger')
        provider = current_user.social_id.split('$')[0]
    
    # Revoke provider access token to force user to authenticate again next time
    oauth = OAuthSignIn.get_provider(provider)
    if 'access_token' in session:
        status_code = oauth.revoke(session.pop('access_token'))
        if status_code not in [200, 204]:
            flash('Failed to revoke access token!'
                  '  Status code: {}'.format(status_code), 'warning')
    else:
        flash("KeyError: 'access_token' not in session; "
              "failed to revoke access token", 'danger')
    logout_user()       # logout current_user
    flash('Logged out.', 'success')
    return redirect(url_for('index'))

# login entry point
# from Miguel Grinberg's https://github.com/miguelgrinberg/flask-oauth-example
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)  # Get provider oauth object
    return oauth.authorize()        # ... and call its authorize function

# Handle callback from provider and login user if authentication successful
# Modified from Miguel Grinberg's
# https://github.com/miguelgrinberg/flask-oauth-example
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)  # Get provider oauth object
    social_id, name, email = oauth.callback()   # call its callback function

    if social_id is None:
        flash('Authentication failed.', 'danger')
        return redirect(url_for('index'))
    # find user by social_id returned
    user = User.query.filter_by(social_id=social_id).first()
    if not user:        # if user doesn't exist, create
        user = User(social_id=social_id)
        # if user is me, give ULTIMATE POWAH
        if social_id == app.config['ROOT_ADMIN_ID']:
            user.administrator = True
        user.name = name
        user.email = email
        db.session.add(user)
        db.session.commit()

    login_user(user, True)
    session['provider'] = provider      # save provider
    flash('Logged in successfully.', 'success')
    return redirect(url_for('index'))


#### JSON and XML Retrieval Functions

# Helper function to construct nested dictionary of todos for serialization
def recurse_make(todo):
        new_todo = todo.serialize
        if not todo.children:
            return new_todo
        child_list = []
        for child in todo.children:
            child_list.append(recurse_make(child))
        new_todo['children'] = child_list
        return new_todo

# provide JSON output of all current_user's todos
@app.route('/todos/json')
@login_required
def todos_json():
    todos = Todo.query.filter_by(parent=None, owner=current_user).all()
    todo_list = []
    for todo in todos:
        todo_list.append(recurse_make(todo))
    return jsonify(todos=todo_list)

# provide JSON output of one todo (plus children)
@app.route('/todos/<int:id>/json')
@login_required
def todo_json(id):
    todo = Todo.query.get(id)
    if todo is None:
        abort(404, 'Todo id {} not found.'.format(id))
    if todo.owner != current_user:
        abort(403, 'You are not authorized to view that todo item')
        return redirect(url_for('index'))
    return jsonify(todo=recurse_make(todo))

# provide JSON output of all users
@app.route('/users/json')
@login_required
def users_json():
    if not current_user.is_admin:
        abort(403, 'You are not authorized to view users.')
    users = User.query.all()
    return jsonify(users=[u.serialize for u in users])

# provide JSON output of one user
@app.route('/users/<int:id>/json')
@login_required
def user_json(id):
    if not current_user.is_admin:
        abort(403, 'You are not authorized to view users.')
    user = User.query.get(id)
    if user is None:
        flash('User id {} not found.'.format(id))
        return redirect(url_for('index'))
    return jsonify(user=user.serialize)

# helper function to make XML response for XML doc.  DRY, ya know
def make_xml_response(xml):
    r = make_response(xml)
    r.headers['Content-Type'] = 'application/xml'
    return r

# provide XML output of all current_user's todos
@app.route('/todos/xml')
@login_required
def todos_xml():
    todos = Todo.query.filter_by(parent=None, owner=current_user).all()
    todo_list = []
    for todo in todos:
        todo_list.append(recurse_make(todo))
    xml = dicttoxml(todo_list, custom_root='todos', attr_type=False)
    xml = xml.replace('item>', 'todo>')     # prefer <todo> tags for list items
    return make_xml_response(xml)

# provide XML output of one todo (plus children)
@app.route('/todos/<int:id>/xml')
@login_required
def todo_xml(id):
    todo = Todo.query.get(id)
    if todo is None:
        abort(404, 'Todo id {} not found.'.format(id))
    if todo.owner != current_user:
        abort(403, 'You are not authorized to view that todo item')
        return redirect(url_for('index'))
    xml = dicttoxml(recurse_make(todo), custom_root='todo', attr_type=False)
    xml = xml.replace('item>', 'todo>')     # prefer <todo> tags for list items
    return make_xml_response(xml)

# provide XML output of all users
@app.route('/users/xml')
@login_required
def users_xml():
    if not current_user.is_admin:
        abort(403, 'You are not authorized to view users.')
    users = User.query.all()
    xml = dicttoxml([u.serialize for u in users], 
                    custom_root='users', attr_type=False)
    xml = xml.replace('item>', 'user>')     # prefer <user> tags for list items
    return make_xml_response(xml)

# provide XML output of one user
@app.route('/users/<int:id>/xml')
@login_required
def user_xml(id):
    if not current_user.is_admin:
        abort(403, 'You are not authorized to view users.')
    user = User.query.get(id)
    if user is None:
        flash('User id {} not found.'.format(id))
        return redirect(url_for('index'))
    xml = dicttoxml(user.serialize, 
                    custom_root='user', attr_type=False)
    return make_xml_response(xml)
