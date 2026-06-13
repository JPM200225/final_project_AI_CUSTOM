import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from backend.server import create_server


class CagCustomTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def get_json(self, path):
        with urlopen(self.url(path), timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def post_json(self, path, payload):
        request = Request(
            self.url(path),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))

    def test_user_without_context_gets_empty_list(self):
        status, body = self.get_json("/api/context?user_id=usuario_nuevo_sin_contexto")

        self.assertEqual(status, 200)
        self.assertEqual(body["context"], [])

    def test_ask_without_context_does_not_use_context(self):
        status, body = self.post_json(
            "/api/ask",
            {"user_id": "usuario_sin_contexto", "question": "Que es RAG en el curso?"},
        )

        self.assertEqual(status, 200)
        self.assertEqual(body["context_used"], [])

    def test_saved_context_persists_across_multiple_keys(self):
        self.post_json(
            "/api/context",
            {"user_id": "carla", "key": "audience", "value": "explicar como principiante"},
        )
        self.post_json(
            "/api/context",
            {"user_id": "carla", "key": "preferred_style", "value": "explicaciones con analogias"},
        )

        status, body = self.get_json("/api/context?user_id=carla")

        self.assertEqual(status, 200)
        self.assertEqual(len(body["context"]), 2)

    def test_ask_uses_preferred_style_analogy(self):
        self.post_json(
            "/api/context",
            {"user_id": "diego", "key": "preferred_style", "value": "explicaciones con analogias"},
        )

        status, body = self.post_json(
            "/api/ask",
            {"user_id": "diego", "question": "Que es CAG?"},
        )

        self.assertEqual(status, 200)
        self.assertIn("preferred_style", body["context_used"])
        self.assertIn("libreta", body["answer"].lower())


if __name__ == "__main__":
    unittest.main()
