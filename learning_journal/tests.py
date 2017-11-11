"""Tests for learning journal."""
from datetime import datetime

from learning_journal.models import Entry

from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import pytest


def test_list_view_returns_list_of_entries_in_dict(dummy_request):
    """Test the entries in the response are in a list."""
    from learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert isinstance(response['entries'], list)


def test_entry_exists_and_is_in_list(dummy_request):
    """Test entry is in the list."""
    from learning_journal.views.default import list_view
    new_entry = Entry(
        title='Test title',
        body='Test body.',
        creation_date=datetime.now()
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    response = list_view(dummy_request)
    assert new_entry.to_dict() in response['entries']


def test_detail_view_shows_entry_detail(dummy_request):
    """Test the detail view shows entry detail."""
    from learning_journal.views.default import detail_view
    new_entry = Entry(
        title='Test title',
        body='Test body.',
        creation_date=datetime.now()
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert response['entry'] == new_entry.to_dict()


def test_detail_view_non_existent_entry(dummy_request):
    """Test non existent entry raises HTTPNotFound error."""
    from learning_journal.views.default import detail_view
    new_entry = Entry(
        title='Test title',
        body='Test body.',
        creation_date=datetime.now()
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 2
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_view_makes_new_entry(dummy_request):
    """Test new entry view makes new entry."""
    from learning_journal.views.default import create_view
    entry_info = {
        "title": "New entry",
        "body": "This is the body"
    }
    dummy_request.method = "POST"
    dummy_request.POST = entry_info
    create_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).first()
    assert entry.title == "New entry"


def test_create_view_on_post_redirects_somewhere(dummy_request):
    """Test new entry will redirect."""
    from learning_journal.views.default import create_view
    entry_info = {
        "title": "New entry",
        "body": "This is the body"
    }
    dummy_request.method = "POST"
    dummy_request.POST = entry_info
    response = create_view(dummy_request)
    assert isinstance(response, HTTPFound)


def test_create_view_returns_dict_with_form_placeholder_on_get(dummy_request):
    """Test create view on POST returns a dict with placeholder text."""
    from learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert response == {'textarea': 'new entry'}


def test_create_view_incomplete_data_placeholder_text(dummy_request):
    """Test an incomplete POST will return text to fill in all inputs."""
    from learning_journal.views.default import create_view
    entry_info = {
        "title": 'Test title',
        "body": ""
    }
    dummy_request.method = "POST"
    dummy_request.POST = entry_info
    response = create_view(dummy_request)
    assert response == {'textarea': 'Title and body requried.'}


def test_delete_has_deleted_data(testapp, fill_the_db):
    """Test that delete view will delete post."""
    response = testapp.get("/journal/3/delete")
    assert 'Test Journal 3' not in response


def test_create_view_successful_post_redirects_home(testapp):
    """Test that a new post will redirect to home view."""
    entry_info = {
        "title": "Test title",
        "body": "Test body"
    }
    response = testapp.post("/journal/new-entry", entry_info)
    assert response.location == 'http://localhost/'


def test_create_view_successful_post_actually_shows_home_page(testapp):
    """Test that a new post will redirect to home view."""
    entry_info = {
        "title": "Sandwich",
        "body": "Test body"
    }
    response = testapp.post("/journal/new-entry", entry_info)
    next_page = response.follow()
    assert "Sandwich" in next_page.ubody


def test_home_status_code_200_ok(testapp):
    """Test that home route has a 200 ok status code."""
    response = testapp.get('/')
    assert response.status_code == 200


def test_non_existent_detail_view_status_code_404(testapp):
    """Test that non-existent detail route has a 404 status code."""
    response = testapp.get('/journal/1111', status=404)
    assert response.status_code == 404


def test_all_entries_in_db_are_on_main_page(testapp, fill_the_db):
    """Test that all the entries in the database are on the main page."""
    response = testapp.get('/')
    html = response.html
    entries = html.find_all('sub')
    assert len(entries) == 20


def test_update_view_redirects_to_detail_view(testapp, fill_the_db):
    """Test that update view will redirect to detail view after update."""
    entry_info = {
        "title": "New title",
        "body": "New body"
    }
    response = testapp.post("/journal/1/edit-entry", entry_info)
    assert response.location == 'http://localhost/journal/1'


def test_403_error_on_new_entry_without_login(testapp_secure):
    """Test for a 403 status code on new entry view if not logged in."""
    assert testapp_secure.get('/journal/new-entry', status=403)


def test_403_error_on_edit_entry_without_login(testapp_secure, fill_the_db):
    """Test for a 403 status code on edit entry view if not logged in."""
    assert testapp_secure.get('/journal/1/edit-entry', status=403)


def test_200_ok_on_detail_view_without_login(testapp_secure, fill_the_db):
    """Test for a 200 status code on detail view if not logged in."""
    assert testapp_secure.get('/journal/1', status=200)


def test_200_ok_on_main_view_without_login(testapp_secure):
    """Test for a 200 status code on main view if not logged in."""
    assert testapp_secure.get('/', status=200)
