import json
from io import BytesIO
from PIL import Image as img
from jose import jwt
import pytest
from pathlib import Path


@pytest.mark.usefixtures('app', 'client', 'dummy_users')
class TestUsersResource:
    def testUsersPost(self, client, dummy_users):
        mockRequestBody = {
            'username': 'test',
            'firstName': 'Johnny',
            'lastName': 'Test',
            'password': 'password',
            'role': {
                'id': 2,
                'name': 'admin'
            }
        }
        data = client.post('/users', json=mockRequestBody)
        assert data.status_code == 201
        assert data.is_json is True
        loadedData = json.loads(data.data)
        assert 'meta' in loadedData.keys()
        data = client.post('/users', json={'username': 'badActor'})
        assert data.status_code == 400
        assert data.is_json is True
        loadedData = json.loads(data.data)
        assert 'meta' in loadedData.keys()

    def testUsersPut(self, client, dummy_users):
        testUsers = [{
            'username': 'list1',
            'firstName': 'Alice',
            'lastName': 'Test',
            'password': 'password',
            'addedBy': 'admin'
        }, {
            'username': 'list2',
            'firstName': 'Bob',
            'lastName': 'Test',
            'password': 'password',
            'addedBy': 'admin'
        }]
        data = client.put('/users', json=testUsers)
        assert data.status_code == 201
        loadedData = json.loads(data.data)
        assert 'meta' in loadedData.keys()
        assert 'users' in loadedData.keys()


@pytest.mark.usefixtures('app', 'client', 'dummy_users')
class TestUserResource:
    def testUserLogin(self, app, client, dummy_users):
        successfulLogin = {'username': 'alicesmith', 'password': 'password'}
        response = client.post('/user', json=successfulLogin)
        data = json.loads(response.data)
        token = data['token']
        headers = response.headers
        decodedToken = jwt.decode(token, app.config['SECRET_KEY'])
        assert 'password' not in decodedToken.keys()
        assert 'sub' in decodedToken.keys()
        assert headers['Authorization'] == 'Bearer ' + token

    def testUserBadLogin(self, app, client, dummy_users):
        badLogin = {'username': 'alicesmith', 'password': 'phony'}
        data = client.post('/user', json=badLogin)
        assert data.status_code == 403

    def testJWTValidateValidHeader(self, app, client, dummy_users):
        tokenData = {
            'firstName': 'Alice',
            'lastName': 'Smith',
            'role': {
                'id': 1,
                'name': 'member'
            },
            'sub': 'alicesmith'
        }
        validJWT = jwt.encode(tokenData, app.config['SECRET_KEY'])
        bearerToken = 'Bearer ' + validJWT
        headers = {'Authorization': bearerToken}
        response = client.get('/user/alicesmith/code', headers=headers)
        responseImage = img.open(BytesIO(response.data))
        testImagePath = Path('./tests/test_qr_code.png')
        referenceImage = img.open(testImagePath)
        assert response.status_code == 200
        assert referenceImage == responseImage

    def testJWTValidateValidBody(self, app, client, dummy_users):
        tokenData = {
            'firstName': 'Alice',
            'lastName': 'Smith',
            'role': {
                'id': 1,
                'name': 'member'
            },
            'sub': 'alicesmith'
        }
        validJWT = jwt.encode(tokenData, app.config['SECRET_KEY'])
        body = json.dumps({'token': validJWT})
        response = client.get('/user/alicesmith/code', json=body)
        responseImage = img.open(BytesIO(response.data))
        testImagePath = Path('./tests/test_qr_code.png')
        referenceImage = img.open(testImagePath)
        assert response.status_code == 200
        assert referenceImage == responseImage
