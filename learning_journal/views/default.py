"""View serve functions."""
from pyramid.view import view_config
import os

HERE = os.path.abspath(__file__)
TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'templates')


@view_config(route_name="home", renderer="templates/index.jinja2")
def list_view(request):
    """Serve the main learning journal page."""
    return{}


@view_config(route_name="post", renderer="templates/detail.jinja2")
def detail_view(request):
    """Serve detail page for single entry."""
    return{}


@view_config(route_name="new-entry", renderer="templates/new_entry.jinja2")
def create_view(request):
    """Serve the create a new entry page."""
    return{}


@view_config(route_name="edit-entry", renderer="templates/edit_entry.jinja2")
def update_view(request):
    """Serve the edit an entry page."""
    return{}
