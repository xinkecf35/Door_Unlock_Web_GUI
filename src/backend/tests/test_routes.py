import json
from jose import jwt
import pytest


@pytest.mark.usefixtures('app', 'client')
class TestUsersResource:

    def testUsersPost(self, client):
        data = client.post('/users', json={
            'username': 'test',
            'firstName': 'Johnny',
            'lastName': 'Test',
            'password': 'password',
            'role': {
                'id': 2,
                'name': 'admin'
            }
        })
        assert data.status_code == 201
        assert data.is_json is True
        loadedData = json.loads(data.data)
        assert 'meta' in loadedData.keys()
        data = client.post('/users', json={
            'username': 'badActor'
        })
        assert data.status_code == 400
        assert data.is_json is True
        loadedData = json.loads(data.data)
        assert 'meta' in loadedData.keys()

    def testUsersPut(self, client):
        testUsers = [
            {
                'username': 'list1',
                'firstName': 'Alice',
                'lastName': 'Test',
                'password': 'password',
                'addedBy': 'test'
            },
            {
                'username': 'list2',
                'firstName': 'Bob',
                'lastName': 'Test',
                'password': 'password',
                'addedBy': 'test'
            }
        ]
        data = client.put('/users', json=testUsers)
        assert data.status_code == 201
        loadedData = json.loads(data.data)
        assert 'meta' in loadedData.keys()
        assert 'users' in loadedData.keys()


@pytest.mark.usefixtures('app', 'client')
class TestUserResource:

    def testUserLogin(self, app, client):
        successfulLogin = {
            'username': 'test',
            'password': 'password'
        }
        data = client.post('/user', json=successfulLogin)
        data = json.loads(data.data)
        token = data['token']
        decodedToken = jwt.decode(token, app.config['SECRET_KEY'])
        assert 'password' not in decodedToken.keys()
        assert 'sub' in decodedToken.keys()
