import unittest
from TKA_recursive import compute_laziest_path


class TestNumber(unittest.TestCase):
    def test_number_1(self):
        response = compute_laziest_path(telephone_number='110')
        desired = (4.0, [('*', '#'), ('1', '#'), ('1', '#'), ('1', '0')])
        self.assertTrue(response == desired)

    def test_number_2(self):
        response = compute_laziest_path(telephone_number='555')
        desired = (2.23606797749979, [('*', '#'), ('5', '#'), ('5', '#'), ('5', '#')])
        self.assertTrue(response == desired)

    def test_number_3(self):
        response = compute_laziest_path(telephone_number='1**')
        desired = (3.605551275463989, [('*', '#'), ('*', '1'), ('*', '1'), ('*', '1')])
        self.assertTrue(response == desired)

    def test_number_4(self):
        response = compute_laziest_path(telephone_number='74147*0#96369')
        passed_dist = response[0]
        true_dist = 12
        self.assertEqual(passed_dist, true_dist)
