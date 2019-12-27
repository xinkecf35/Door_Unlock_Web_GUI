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

    def testUserSchema(self, ma, db):
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
            role=adminRole.id
        )
        db.session.add(testAdminPerson)
        db.session.commit()
        userSchema = UserSchema()
        dumpInfo = userSchema.dumps(testAdminPerson)
        loadedDump = json.loads(dumpInfo)
        for key in loadedDump.keys():
            assert loadedDump[key] == referenceData[key]
