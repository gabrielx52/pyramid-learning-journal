"""Routes with URIs for learning jouranl."""


def includeme(config):
    """Route for pyramid learning journal."""
    config.add_static_view('static', 'static', cache_max_age=30)
    config.add_route('home', '/')
    config.add_route('post', '/journal/{id:\d+}')
    config.add_route('new-entry', '/journal/new-entry')
    config.add_route('delete', '/journal/{id:\d+}/delete')
    config.add_route('edit-entry', '/journal/{id:\d+}/edit-entry')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
