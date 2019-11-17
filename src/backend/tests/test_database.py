import pytest
import names
from random import randint
from src.database.Person import Person
from src.database.Role import Role


@pytest.mark.usefixtures('db')
class TestPerson:
    def generateName(self):
        firstName = names.get_first_name()
        lastName = names.get_last_name()
        username = ''.join([firstName, lastName, str(randint(1, 1000))])
        return (firstName, lastName, username)

    def testInsert(self, db):
        role1 = Role(name='member',
                     canUnlock=1,
                     canManage=0,
                     canAccessHistory=0)
        db.session.add(role1)

        persons = []
        names = []
        for _ in range(10):
            data = self.generateName()
            names.append(data)
            persons.append(Person(firstName=data[0],
                                  lastName=data[1],
                                  username=data[2]))
        for person in persons:
            db.session.add(person)
        for name in names:
            testUsername = name[2]
            queryPerson = Person.query.filter_by(username=testUsername).first()
            assert queryPerson.username == testUsername
