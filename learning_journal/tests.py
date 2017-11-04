"""Tests for learning journal."""
import pytest
import transaction

from pyramid import testing
from learning_journal.models import Entry, get_tm_session
from learning_journal.models.meta import Base
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound, HTTPFound


@pytest.fixture
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/LearningJournal'
    })
    config.include("learning_journal.models")
    config.include("learning_journal.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session."""
    session_factory = configuration.registry["dbsession_factory"]
    session = session_factory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Fake HTTP Request."""
    return testing.DummyRequest(dbsession=db_session)


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


@pytest.fixture(scope="session")
def testapp(request):
    """Test app for learning journal tests."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/LearningJournal'
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.routes')
        config.include('learning_journal.models')
        config.scan()
        return config.make_wsgi_app()

    app = main()

    session_factory = app.registry["dbsession_factory"]
    engine = session_factory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return TestApp(app)


@pytest.fixture(scope="session")
def fill_the_db(testapp):
    """Fill the db for the testapp."""
    session_factory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        dbsession.add_all(ENTRIES)

ENTRIES = []
for i in range(1, 20):
    new_entry = Entry(
        title='Test Journal {}'.format(i),
        body='Test body'
    )
    ENTRIES.append(new_entry)


def test_detail_route_has_entry_data(testapp, fill_the_db):
    """Test that an entry's detail page has data."""
    response = testapp.get("/journal/3")
    assert 'Test Journal 3' in response


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
