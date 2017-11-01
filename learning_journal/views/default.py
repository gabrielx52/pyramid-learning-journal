"""View serve functions."""

from pyramid.response import Response
import os

HERE = os.path.abspath(__file__)
TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'templates')


def list_view(request):
    """Serve the main learning journal page."""
    with open(os.path.join(TEMPLATE, "index.html")) as file:
        return Response(file.read())


def detail_view(request):
    """Serve detail page for single entry."""
    with open(os.path.join(TEMPLATE, "detail.html")) as file:
        return Response(file.read())


def create_view(request):
    """Serve the create a new entry page."""
    with open(os.path.join(TEMPLATE, "new_entry.html")) as file:
        return Response(file.read())


def update_view(request):
    """Serve the edit an entry page."""
    with open(os.path.join(TEMPLATE, "edit_entry.html")) as file:
        return Response(file.read())
