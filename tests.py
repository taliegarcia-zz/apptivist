"""Sample test suite for testing demo."""

import server
import unittest

class MyAppIntegrationTestCase(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def setUp(self):
        print "(setUp ran)"
        self.app = server.app.test_client()

    def tearDown(self):
        # We don't need to do anything here; we could just
        # not define this method at all, but have a stub
        # here as an example.
        print "(tearDown ran)"

    def test_home(self):
        result = self.app.get('/')
        self.assertIn('<h1>Apptivist</h1>', result.data)

    def test_results(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<sh1>Apptivist</h1>', result.data)


if __name__ == '__main__':
    # If called like a script, run our tests

    unittest.main()
