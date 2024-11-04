import unittest
from my_tools.connect_check import ConnectivityChecker

class TestConnectivityChecker(unittest.TestCase):
    def setUp(self):
        self.checker = ConnectivityChecker("https://www.example.com")

    def test_http_status(self):
        status, message = self.checker.check_http_status()
        self.assertTrue(status)
        self.assertIn("200", message)

    def test_dns(self):
        status, message = self.checker.check_dns()
        self.assertTrue(status)

    def test_invalid_url(self):
        checker = ConnectivityChecker("https://invalid-domain-name-that-does-not-exist.com")
        status, message = checker.check_dns()
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main() 