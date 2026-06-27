"""Tests for the pi calculation module."""

import unittest
from pi import calculate_pi


class TestCalculatePi(unittest.TestCase):
    """Test cases for the calculate_pi function."""

    def test_pi_to_5_decimal_places(self):
        """Test that pi is correctly calculated to 5 decimal places."""
        result = calculate_pi(5)
        self.assertEqual(result, 3.14159)

    def test_pi_to_2_decimal_places(self):
        """Test that pi is correctly calculated to 2 decimal places."""
        result = calculate_pi(2)
        self.assertEqual(result, 3.14)

    def test_pi_to_0_decimal_places(self):
        """Test that pi rounded to 0 decimal places is 3."""
        result = calculate_pi(0)
        self.assertEqual(result, 3.0)

    def test_default_precision(self):
        """Test that the default precision is 5 decimal places."""
        result = calculate_pi()
        self.assertEqual(result, 3.14159)

    def test_return_type_is_float(self):
        """Test that the return type is a float."""
        result = calculate_pi()
        self.assertIsInstance(result, float)


if __name__ == "__main__":
    unittest.main()
