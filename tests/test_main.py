import unittest
from fastapi.testclient import TestClient

from main import app, ProcessingStatus

client = TestClient(app)


class TestTaskManagement(unittest.TestCase):
    def setUp(self):
        self.client = client

    def test_create_task(self):
        response = self.client.post(
            "/tasks",
            json={
                "user_id": "test_user",
                "description": "Send welcome email"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["status"], ProcessingStatus.NEW.value)

    def test_retrieve_task_by_id(self):
        response = self.client.post(
            "/tasks",
            json={"user_id": "test_user", "description": "Fetch by ID"}
        )
        task_id = response.json()["id"]

        res = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id"], task_id)
        self.assertEqual(data["description"], "Fetch by ID")

    def test_list_all_tasks(self):
        self.client.post("/tasks", json={"user_id": "ana", "description": "A"})
        self.client.post("/tasks", json={"user_id": "bob", "description": "B"})

        res = self.client.get("/tasks")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_filter_tasks_by_status(self):
        self.client.post("/tasks", json={"user_id": "tester", "description": "To filter"})

        res = self.client.get("/tasks", params={"status": ProcessingStatus.NEW.value})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(all(task["status"] == ProcessingStatus.NEW.value for task in data))

    def test_nonexistent_task_returns_none(self):
        res = self.client.get("/tasks/does-not-exist-id")
        self.assertEqual(res.status_code, 200)
        self.assertIsNone(res.json())
