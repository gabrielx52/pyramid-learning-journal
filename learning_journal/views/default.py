"""View serve functions."""
from datetime import datetime

from learning_journal.models.mymodel import Entry
from learning_journal.security import is_authenticated

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import NO_PERMISSION_REQUIRED, forget, remember
from pyramid.view import view_config


@view_config(route_name="home", renderer="templates/index.jinja2")
def list_view(request):
    """Serve the main learning journal page."""
    entries = request.dbsession.query(Entry).all()
    entries = [entry.to_dict() for entry in entries]
    return {
        "entries": entries
    }


@view_config(route_name="post", renderer="templates/detail.jinja2")
def detail_view(request):
    """Serve detail page for single entry."""
    post_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(post_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        return {
            'entry': entry.to_dict()
        }
    if request.method == "POST":
        return HTTPFound(request.route_url('edit-entry', id=post_id))


@view_config(route_name="new-entry",
             renderer="templates/new_entry.jinja2",
             permission="secret")
def create_view(request):
    """Serve the create a new entry page."""
    if request.method == "GET":
        return{
            'textarea': 'new entry'
        }
    if request.method == "POST":
        if len(request.POST['title']) == 0 or len(request.POST['body']) == 0:
            return {
                'textarea': 'Title and body requried.'
            }
        print(request.POST)
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body'],
            creation_date=datetime.now()
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('home'))


@view_config(route_name="edit-entry",
             renderer="templates/edit_entry.jinja2",
             permission="secret")
def update_view(request):
    """Serve the edit an entry page."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound
    if request.method == "GET":
        return {
            'entry': entry.to_dict()
        }
    if request.method == "POST":
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        entry.creation_date = datetime.now()
        request.dbsession.add(entry)
        request.dbsession.flush()
        return HTTPFound(request.route_url('post', id=entry.id))


@view_config(route_name="delete",
             permission="secret")
def delete_view(request):
    """Delete journal entry."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entry).get(entry_id)
    if not entry:
        raise HTTPNotFound
    request.dbsession.delete(entry)
    return HTTPFound(request.route_url('home'))


@view_config(
    route_name='login',
    renderer="learning_journal:templates/login.jinja2",
    permission=NO_PERMISSION_REQUIRED
)
def login(request):
    """Login view."""
    if request.authenticated_userid:
        return HTTPFound(request.route_url('home'))
    if request.method == "GET":
        return {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if is_authenticated(username, password):
            headers = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=headers)

        return {
            'error': 'Incorrect username/password combination.'
        }


@view_config(route_name='logout')
def logout(request):
    """Logout route."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
