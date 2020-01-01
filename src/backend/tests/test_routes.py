import pytest


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
