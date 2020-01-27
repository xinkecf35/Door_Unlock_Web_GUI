import json
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

    def testUserLogin(self, client):
        successfulLogin = {
            'username': 'test',
            'password': 'password'
        }
        client.post('/user', json=successfulLogin)
