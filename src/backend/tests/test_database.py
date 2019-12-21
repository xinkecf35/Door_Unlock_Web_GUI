import pytest
import names
from random import randint
from src.database.Person import Person
from src.database.Role import Role
from src.database.Admin import Admin
from sqlalchemy.exc import IntegrityError


@pytest.mark.usefixtures('db')
class TestPerson:
    def generateName(self):
        firstName = names.get_first_name()
        lastName = names.get_last_name()
        username = ''.join([firstName, lastName, str(randint(1, 1000))])
        return (firstName, lastName, username)

    def testInsert(self, db):
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

        testAdminPerson = Person(
            firstName='John',
            lastName='Smith',
            username='admin',
            role=role2.id)
        db.session.add(testAdminPerson)
        db.session.commit()
        testAdmin = Admin(
            id=testAdminPerson.id,
            password='snakeoil')
        db.session.add(testAdmin)
        persons = []
        names = []
        insertedAdmin = Person.query.filter_by(username='admin').first()
        for _ in range(10):
            data = self.generateName()
            names.append(data)
            persons.append(Person(firstName=data[0],
                                  lastName=data[1],
                                  username=data[2],
                                  addedBy=insertedAdmin.id))
        for person in persons:
            db.session.add(person)
        db.session.commit()
        for name in names:
            testUsername = name[2]
            queryPerson = Person.query.filter_by(username=testUsername).first()
            assert queryPerson.username == testUsername
            assert queryPerson.addedBy == testAdminPerson.id

        # Attempt to create user that does not have foreign key available
        fkTestPerson = Person(
            firstName='Alice',
            lastName='Invalid',
            username='invalidalice',
            role=3
        )
        with pytest.raises(IntegrityError):
            db.session.add(fkTestPerson)
            db.session.commit()
