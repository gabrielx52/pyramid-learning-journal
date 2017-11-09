"""Tests fixtures for learning journal."""
import pytest
import transaction

from pyramid import testing
from learning_journal.models import Entry, get_tm_session
from learning_journal.models.meta import Base


@pytest.fixture
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/test_LearningJournal'
    })
    config.include("learning_journal.models")
    config.include("learning_journal.routes")
    # config.include("learning_journal.security")

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


@pytest.fixture(scope="session")
def testapp(request):
    """Test app for learning journal tests."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/test_LearningJournal'
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
def testapp_secure(request):
    """Test app with security for learning journal tests."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/test_LearningJournal'
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.routes')
        config.include('learning_journal.models')
        config.include("learning_journal.security")
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
