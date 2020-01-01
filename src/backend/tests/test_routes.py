import pytest
import json

@pytest.mark.usefixtures('app', 'client')
class TestUsersResource:

    def testUsersPost(self, client):
        data = client.post('/users', json={
            'username': 'test',
            'firstName': 'Johnny',
            'lastName': 'Test',
            'password': 'password',
        })
        assert data.status_code == 200
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
