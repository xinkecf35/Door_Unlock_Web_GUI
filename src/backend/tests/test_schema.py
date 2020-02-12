import json
import pytest
from door_api.database import Person, Role
from marshmallow import ValidationError
from door_api.models import UserSchema
from door_api.models import JWTSchema


@pytest.mark.usefixtures('db', 'ma', 'dummy_users')
class TestUserSchema:
    def fetchRoles(self, db):
        roles = Role.query.all()
        return roles[0], roles[1]

    def testUserSchemaDump(self, db, ma, dummy_users):
        memberRole, adminRole = self.fetchRoles(db)
        referenceData = {
            'username': 'johnadmin',
            'firstName': 'John',
            'lastName': 'Smity'
        }
        testAdminPerson = Person(
            firstName='John',
            lastName='Smity',
            username='johnadmin',
            password='password',
            roleId=adminRole.id
        )
        excludedFields = ['password', 'admin', 'created']
        userSchema = UserSchema(exclude=excludedFields)
        db.session.add(testAdminPerson)
        db.session.commit()
        dumpInfo = userSchema.dumps(testAdminPerson)
        loadedDump = json.loads(dumpInfo)
        for key in referenceData.keys():
            assert loadedDump[key] == referenceData[key]
        assert 'password' not in loadedDump.keys()

    def testUserInsertFromData(self, db, ma, dummy_users):
        insertFromData = {
            'username': 'test',
            'firstName': 'Johnny',
            'lastName': 'Test',
            'password': 'password',
            'addedBy': 'admin'
        }
        userSchema = UserSchema()
        userModelFromData = userSchema.load(insertFromData)
        db.session.add(userModelFromData)
        db.session.commit()
        dumpedUser = userSchema.dump(userModelFromData)
        assert userModelFromData.id is not None
        assert userModelFromData.validatePassword('password')
        assert type(dumpedUser['addedBy']) is str
        adminInsertFromData = {
            'username': 'admininsert',
            'firstName': 'Admin',
            'lastName': 'Smith',
            'password': 'password',
            'role': {
                'id': 2,
                'name': 'admin'
            }
        }
        testAdminInsert = userSchema.load(adminInsertFromData)
        db.session.add(testAdminInsert)
        db.session.commit()
        assert testAdminInsert.id is not None
        assert testAdminInsert.validatePassword('password')
        nonExistentUserData = {
            'username': 'invalidAdded',
            'firstName': 'Bob',
            'lastName': 'Invalid',
            'password': 'password',
            'addedBy': '404'
        }
        with pytest.raises(ValidationError):
            userSchema.load(nonExistentUserData)

    def testNestedAddedBy(self, db, ma, dummy_users):
        nestedUserData = {
            'username': 'nestedAdd',
            'firstName': 'Zach',
            'lastName': 'Nested',
            'password': 'password',
            'addedBy': 'admin'
        }
        userSchema = UserSchema()
        nestedUser = userSchema.load(nestedUserData)
        db.session.add(nestedUser)
        db.session.commit()
        nestedDump = userSchema.dump(nestedUser)
        assert nestedDump['addedBy'] == 'admin'

    def testUpdateFromLoad(self, db, ma):
        testUsername = 'bobsmith'
        testId = Person.query.filter_by(username=testUsername).first().id
        updatedPassword = 'snakeoil'
        updateWithData = {
            'id': testId,
            'username': testUsername,
            'firstName': 'Johnny',
            'lastName': 'Test',
            'password': updatedPassword,
            'addedBy': 'admin'
        }
        userSchema = UserSchema()
        updatedUser = userSchema.load(updateWithData)
        db.session.commit()
        assert updatedUser.id == testId
        assert updatedUser.validatePassword(updatedPassword)

    def testWithInvalidRole(self, db, ma):
        badActorData = {
            'username': 'hacker',
            'firstName': 'Johnny',
            'lastName': 'Test',
            'password': 'updatedPassword',
            'addedBy': 'johnadmin',
            'role': {
                'id': 3,
                'name': 'SuperAdmin'
            }
        }
        userSchema = UserSchema()
        with pytest.raises(ValidationError):
            userSchema.load(badActorData)


@pytest.mark.usefixtures('db', 'ma', 'dummy_users')
class TestJWTSchema:

    def testJWTDump(self, db, ma, dummy_users):
        testUsername = 'bobsmith'
        test = Person.query.filter_by(username=testUsername).first()
        jwtSchema = JWTSchema()
        jwtDump = jwtSchema.dump(test)
        assert len(jwtDump.keys()) == 4
        assert 'password' not in jwtDump.keys()
