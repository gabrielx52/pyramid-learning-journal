"""Tests for learning journal."""
import pytest

from pyramid import testing
from learning_journal.models import Entry
from learning_journal.models.meta import Base
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound


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
