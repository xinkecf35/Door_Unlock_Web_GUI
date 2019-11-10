import pytest
from src.database.Person import Person
from src.database.Role import Role

@pytest.mark.usefixtures('db')
class TestPerson:

    def testInsert(self, db):
        role1 = Role(name='member',
                     canUnlock=1,
                     canManage=0,
                     canAccessHistory=0)
        db.session.add(role1)
        person1 = Person(firstName='John',
                         lastName='Doe',
                         username='johndoe001')
        person2 = Person(firstName='Jane',
                         lastName='Doe',
                         username='janedoe001')
        assert person1.firstName == 'John'
        assert person2.firstName == 'Jane'
        db.session.add(person1)
        db.session.add(person2)
        db.session.commit()
        query1 = Person.query.filter_by(firstName='John').first()
        print(query1)
