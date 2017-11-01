"""Tests for learning journal."""
from pyramid import testing
import pytest


@pytest.fixture
def dummy_request():
    """Set up a dummy request for testing."""
    return testing.DummyRequest()


def test_list_view_status_code_200():
    """Check if list view has a 200 code."""
    from .views import list_view
    req = dummy_request()
    response = list_view(req)
    assert response.status_code == 200


def test_detail_view_status_code_200():
    """Check if detail view has a 200 code."""
    from .views import detail_view
    req = dummy_request()
    response = detail_view(req)
    assert response.status_code == 200


def test_create_view_status_code_200():
    """Check if create view has a 200 code."""
    from .views import create_view
    req = dummy_request()
    response = create_view(req)
    assert response.status_code == 200


def test_update_view_status_code_200():
    """Check if update view has a 200 code."""
    from .views import update_view
    req = dummy_request()
    response = update_view(req)
    assert response.status_code == 200
