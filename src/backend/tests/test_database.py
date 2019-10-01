import pytest
from src.database.Person import Person


class TestPerson:

    def testInsert(app):
        person1 = Person(firstName='John', lastName='Doe')
        assert person1.firstName == 'John'
