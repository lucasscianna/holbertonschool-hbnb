import unittest
from app import create_app

class TestHBnBAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test_user_creation_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@hbnb.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_user_creation_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "mauvais-format"
        })
        self.assertEqual(response.status_code, 400)

    def test_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": -10.0,
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": "dummy-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Super!",
            "rating": 7,
            "user_id": "u-id",
            "place_id": "p-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_non_existent_user(self):
        response = self.client.get('/api/v1/users/id-imaginaire')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
