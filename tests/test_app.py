import unittest

from auto_reply_bot.app import create_app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Message Tester", response.data)

    def test_health_endpoint_returns_status(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_api_reply_returns_rule_match(self):
        response = self.client.post("/api/reply", json={"message": "this is urgent"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("immediate attention", response.get_json()["reply"])


if __name__ == "__main__":
    unittest.main()
