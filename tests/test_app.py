# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert "About Me" in html
        assert "Work Experience" in html
        assert "Education" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        # Test POST endpoint for timeline
        post_response = self.client.post("/api/timeline_post", data=
            {"name": "Tom Bow", "email": "tom@example.com", "content": "Another test!"})
        assert post_response.status_code == 200
        assert response.is_json

        # Test that timeline post was successfully added to database with GET endpoint
        get_response = self.client.get("/api/timeline_post")
        assert get_response.is_json
        get_json = get_response.get_json()
        entry = get_json["timeline_posts"][0]
        assert entry["name"] == "Tom Bow"
        assert entry["email"] == "tom@example.com"
        assert entry["content"] == "Another test!"

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post",
                                    data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", 
                                    data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", 
                                    data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
