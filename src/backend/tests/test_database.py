from src.database.Person import Person


class TestPerson:

    def testInsert(db):
        person1 = Person(firstName='John', lastName='Doe')
        person1 = Person(firstName='Jane', lastName='Doe')
        assert person1.firstName == 'John'
