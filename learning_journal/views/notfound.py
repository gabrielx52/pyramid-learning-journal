"""404 not found view."""
from pyramid.view import notfound_view_config


@notfound_view_config(renderer='../templates/404.jinja2')
def notfound_view(request):
    """404 page not found."""
    request.response.status = 404
    return {}
