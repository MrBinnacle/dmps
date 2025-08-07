"""
Tests for the main module.
"""
import unittest
from dmps.main import hello_world

class TestMain(unittest.TestCase):
    """Test cases for the main module."""
    
    def test_hello_world(self):
        """Test the hello_world function."""
        self.assertEqual(hello_world(), "Hello, World!")

if __name__ == "__main__":
    unittest.main()
