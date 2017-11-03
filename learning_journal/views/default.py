"""View serve functions."""
from learning_journal.data.entries import ENTRIES
from learning_journal.models.mymodel import Entry
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
    # for entry in ENTRIES:
    #     if entry['id'] == post_id:
    #         return{'entry': entry}
    entry = request.dbsession.query(Entry).get(post_id)
    return {
        'entry': entry.to_dict()
    }


@view_config(route_name="new-entry", renderer="templates/new_entry.jinja2")
def create_view(request):
    """Serve the create a new entry page."""
    return{}


@view_config(route_name="edit-entry", renderer="templates/edit_entry.jinja2")
def update_view(request):
    """Serve the edit an entry page."""
    return{}
