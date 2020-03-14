import pytest
import yaml


@pytest.fixture()
def app(request):
    # load config from yaml file
    with open('tests/config.yaml', 'r') as configFile:
        config = yaml.safe_load(configFile)
    from door_api import create_app
    app = create_app(config)
    return app


@pytest.fixture()
def db(app):
    from door_api.extensions import db
    db.app = app
    with app.app_context():
        db.create_all()
        yield db
        db.session.rollback()


@pytest.fixture()
def ma(app, db):
    from door_api.extensions import ma
    ma.app = app
    with app.app_context():
        yield ma


@pytest.fixture()
def client(app):
    from door_api.extensions import db
    with app.test_client() as client:
        db.app = app
        db.create_all()
        with app.app_context():
            yield client


@pytest.fixture()
def dummy_users(db):
    from door_api.database import Person
    adminUser = Person(firstName='John',
                       lastName='Smith',
                       username='admin',
                       password='snakeoil',
                       roleId=2)
    testUser1 = Person(firstName='Alice',
                       lastName='Smith',
                       username='alicesmith',
                       password='password',
                       addedBy=1)
    testUser2 = Person(firstName='Bob',
                       lastName='Smith',
                       username='bobsmith',
                       password='password1',
                       addedBy=1)
    db.session.add(adminUser)
    db.session.commit()
    db.session.add(testUser1)
    db.session.add(testUser2)
    db.session.commit()
