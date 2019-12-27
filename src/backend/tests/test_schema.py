import json
import pytest
from src.database.Person import Person
from src.database.Role import Role
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
            'lastName': 'Smity',
            'addedBy': None
        }
        testAdminPerson = Person(
            firstName='John',
            lastName='Smity',
            username='johnadmin',
            password='password',
            roleId=adminRole.id
        )
        userSchema = UserSchema(exclude=['password', 'id'])
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
            'addedBy': None,
        }
        userSchema = UserSchema()
        userModelFromData = userSchema.load(insertFromData)
        db.session.add(userModelFromData)
        db.session.commit()
        assert userModelFromData.id is not None
        assert userModelFromData.validatePassword('password')
