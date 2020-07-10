from django.test import TestCase
from app.calc import add, subtract


class CalcTest(TestCase):
    """ Notice that def func's below should be stated with test_ """
    def test_add_number(self):
        """ Test that two number are added together """
        self.assertEqual(add(3, 8), 11)

    def test_subtract_numbers(self):
        """ Test that values are subtracted an returned """
        self.assertEqual(subtract(5, 11), 6)
