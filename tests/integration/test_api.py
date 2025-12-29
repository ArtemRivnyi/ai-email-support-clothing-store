import unittest
import json
from api.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        # Note: This test might fail if Redis/Ollama are not actually running locally
        # In a real CI environment, we'd spin up service containers.
        # For now, we expect 503 if services are down, or 200 if up.
        # We just check that the endpoint responds.
        response = self.app.get('/health')
        self.assertIn(response.status_code, [200, 503])
        data = json.loads(response.data)
        self.assertIn('status', data)

    def test_metrics_endpoint(self):
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'emails_processed_total', response.data)

if __name__ == '__main__':
    unittest.main()
