"""View serve functions."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from learning_journal.models.mymodel import Entry


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
    if entry:
        return {
            'entry': entry.to_dict()
        }
    raise HTTPNotFound


@view_config(route_name="new-entry", renderer="templates/new_entry.jinja2")
def create_view(request):
    """Serve the create a new entry page."""
    return{}


@view_config(route_name="edit-entry", renderer="templates/edit_entry.jinja2")
def update_view(request):
    """Serve the edit an entry page."""
    return{}
