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
        print(data.get_json())
        assert data.status_code == 200
