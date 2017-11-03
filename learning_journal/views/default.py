"""View serve functions."""
import os

from learning_journal.data.entries import ENTRIES

from pyramid.view import view_config


@view_config(route_name="home", renderer="templates/index.jinja2")
def list_view(request):
    """Serve the main learning journal page."""
    return{"entries": ENTRIES}


@view_config(route_name="post", renderer="templates/detail.jinja2")
def detail_view(request):
    """Serve detail page for single entry."""
    post_id = int(request.matchdict['id'])
    # import pdb; pdb.set_trace()
    for entry in ENTRIES:
        if entry['id'] == post_id:
            return{'entry': entry}


@view_config(route_name="new-entry", renderer="templates/new_entry.jinja2")
def create_view(request):
    """Serve the create a new entry page."""
    return{}


@view_config(route_name="edit-entry", renderer="templates/edit_entry.jinja2")
def update_view(request):
    """Serve the edit an entry page."""
    return{}
