import pytest
import yaml


@pytest.fixture(scope='module')
def app(request):
    # load config from yaml file
    with open('tests/config.yaml', 'r') as configFile:
        config = yaml.safe_load(configFile)
    from src.app import create_app
    app = create_app(config)
    return app


@pytest.fixture(scope='module')
def db(app):
    from src.extensions import db
    db.app = app
    with app.app_context():
        db.create_all()
        yield db
        db.session.rollback()


@pytest.fixture(scope='module')
def ma(app, db):
    from src.extensions import ma
    ma.app = app
    with app.app_context():
        yield ma


@pytest.fixture()
def client(app):
    from src.extensions import db
    with app.test_client() as client:
        db.app = app
        db.create_all()
        with app.app_context():
            yield client
