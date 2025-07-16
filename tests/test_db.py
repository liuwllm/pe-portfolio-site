# test_db.py

import unittest
import os
os.environ['TESTING'] = 'true'

from peewee import *
from app import TimelinePost, app

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe',
                                         email='john@example.com', 
                                         content='Hello world, I\'m John!')
        assert first_post.id == 1

        second_post = TimelinePost.create(name='Jane Doe',
                                          email='jane@example.com', 
                                          content='Hello world, I\'m Jane!')
        assert second_post.id == 2

        # Get timeline posts and assert that they are correct
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2
        
        # Check that posts are in descending order (newest first)
        assert json["timeline_posts"][0]["name"] == "Jane Doe"
        assert json["timeline_posts"][1]["name"] == "John Doe"

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
