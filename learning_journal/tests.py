"""Tests for learning journal."""
from pyramid.testing import DummyRequest
import pytest


@pytest.fixture
def dummy_request():
    """Set up a dummy request for testing."""
    return DummyRequest()


def test_list_view_returns_list_of_entries_in_dict(dummy_request):
    """Test if entries dict is in list view."""
    from learning_journal.views.default import list_view
    req = dummy_request
    response = list_view(req)
    assert 'entries' in response


@pytest.fixture
def testapp():
    """Test app fixture."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()
    return TestApp(app)


def test_detail_route_has_title(testapp):
    """Test detail has a title in the response."""
    response = testapp.get('/journal/13')
    assert 'title' in response


def test_entry_13_body_has_entry_text(testapp):
    """Test detail page has specific text in body."""
    response = testapp.get('/journal/13')
    assert b'provided documentation' in response.body


def test_entry_1_body_has_entry_text(testapp):
    """Test detail page has specific text in body."""
    response = testapp.get('/journal/1')
    assert b'extra packages' in response.body
