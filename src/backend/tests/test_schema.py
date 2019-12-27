import json
import pytest
from src.database.Person import Person
from src.database.Role import Role
from marshmallow import ValidationError
from src.models.UserSchema import UserSchema


@pytest.mark.usefixtures('db', 'ma')
class TestUserSchema:
    def insertRoles(self, db):
        role1 = Role(
            name='member',
            canUnlock=1,
            canManage=0,
            canAccessHistory=0)
        role2 = Role(
            name='admin',
            canUnlock=1,
            canManage=1,
            canAccessHistory=1)
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()
        return role1, role2

    def testUserSchemaDump(self, db, ma):
        memberRole, adminRole = self.insertRoles(db)
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
        excludedFields = ['password', 'id', 'admin', 'created']
        userSchema = UserSchema(exclude=excludedFields)
        db.session.add(testAdminPerson)
        db.session.commit()
        dumpInfo = userSchema.dumps(testAdminPerson)
        loadedDump = json.loads(dumpInfo)
        for key in referenceData.keys():
            assert loadedDump[key] == referenceData[key]
        assert 'id' not in loadedDump.keys()
        assert 'password' not in loadedDump.keys()

    def testUserInsertFromData(self, db, ma):
        insertFromData = {
            'username': 'test',
            'firstName': 'Johnny',
            'lastName': 'Test',
            'password': 'password',
            'addedBy': 'johnadmin'
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

    def testNestedAddedBy(self, db, ma):
        nestedUserData = {
            'username': 'nestedAdd',
            'firstName': 'Zach',
            'lastName': 'Nested',
            'password': 'password',
            'addedBy': 'test'
        }
        userSchema = UserSchema()
        nestedUser = userSchema.load(nestedUserData)
        db.session.add(nestedUser)
        db.session.commit()
        nestedDump = userSchema.dump(nestedUser)
        assert nestedDump['addedBy'] == 'test'
