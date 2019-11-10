import pytest
import yaml


@pytest.fixture(scope='session')
def app(request):
    # load config from yaml file
    with open('tests/config.yaml', 'r') as configFile:
        config = yaml.safe_load(configFile)
    from src.app import create_app
    app = create_app(config)
    return app


@pytest.fixture(scope='session')
def db(app):
    from src.extensions import db
    db.app = app
    with app.app_context():
        db.create_all()
        yield db
