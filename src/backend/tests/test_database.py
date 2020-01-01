import pytest
import names
from random import randint
from door_api.database import Person
from door_api.database import Role
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError


@pytest.mark.usefixtures('db')
class TestPerson:
    def generateName(self):
        firstName = names.get_first_name()
        lastName = names.get_last_name()
        username = ''.join([firstName, lastName, str(randint(1, 1000))])
        return (firstName, lastName, username)

    def fetchRoles(self, db):
        roles = Role.query.all()
        return roles[0], roles[1]

    def testInsertPersonAdmin(self, db):
        role1, role2 = self.fetchRoles(db)
        testAdminPerson = Person(
            firstName='John',
            lastName='Smith',
            username='admin',
            password='snakeoil',
            roleId=role2.id)
        db.session.add(testAdminPerson)
        db.session.commit()
        assert testAdminPerson.password != 'snakeoil'
        assert testAdminPerson.validatePassword('snakeoil')
        assert testAdminPerson.validatePassword('password') is False

    def testPersonInsertWithAdmin(self, db):
        persons = []
        names = []
        testAdminPerson = Person.query.filter_by(username='admin').first()
        for _ in range(10):
            data = self.generateName()
            names.append(data)
            person = Person(
                firstName=data[0],
                lastName=data[1],
                username=data[2],
                password='password',
                addedBy=testAdminPerson.id)
            persons.append(person)
        for person in persons:
            db.session.add(person)
        db.session.commit()
        lastHash = b'0'
        for name in names:
            testUsername = name[2]
            queryPerson = Person.query.filter_by(username=testUsername).first()
            assert queryPerson.username == testUsername
            assert queryPerson.addedBy == testAdminPerson.id
            assert queryPerson.validatePassword('password')
            assert queryPerson.password != lastHash
            lastHash = queryPerson.password

        # Attempt to create user that does not have foreign key available,
        # should fail to do so.
        fkTestPerson = Person(
            firstName='Alice',
            lastName='Invalid',
            username='invalidalice',
            password='password',
            roleId=3
        )
        with pytest.raises(IntegrityError):
            db.session.add(fkTestPerson)
            db.session.commit()
        db.session.rollback()

    def testRolesFetch(self, db):
        personsCount = db.session.query(
            func.count(Person.id)).\
            join(Role).filter(Role.name == 'member').all()
        assert personsCount[0][0] == 10
        adminCount = db.session.query(
            func.count(Person.id)).\
            join(Role).filter(Role.name == 'admin').all()
        assert adminCount[0][0] == 1
