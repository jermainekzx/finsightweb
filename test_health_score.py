# tests for the health_score function in web.py
# pure logic, no database or network needed
import unittest
from web import health_score

class TestHealthScore(unittest.TestCase):
    def test_low_risk(self):
        result = health_score(0.5, 2.0, 4)
        self.assertEqual(result, "LOW RISK")

    def test_medium_risk(self):
        result = health_score(1.5, 1.2, 2.5)
        self.assertEqual(result, "MEDIUM RISK")

    def test_high_risk(self):
        result = health_score(3.0, 0.5, 1.0)
        self.assertEqual(result, "HIGH RISK")

    def test_borderline_de_ratio_pushes_to_high(self):
        # de ratio of exactly 2 fails the medium risk check (de_ratio < 2)
        result = health_score(2.0, 1.5, 3)
        self.assertEqual(result, "HIGH RISK")

if __name__ == '__main__':
    unittest.main()