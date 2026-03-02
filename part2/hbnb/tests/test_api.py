import unittest
from app import create_app

class TestHBnBAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # --- SECTION A: USERS ---
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
            "email": "invalid-mail"
        })
        self.assertEqual(response.status_code, 400)

    def test_user_missing_fields(self):
        """Test champ obligatoire vide (first_name)"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Smith",
            "email": "test@hbnb.com"
        })
        self.assertEqual(response.status_code, 400)

    # --- SECTION B: PLACES ---
    def test_place_invalid_price_negative(self):
        """Test prix négatif"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": -10.0,
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": "dummy-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_place_invalid_price_type(self):
        """Test prix de type string"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": "cent",
            "latitude": 45.0,
            "longitude": 1.0,
            "owner_id": "dummy-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_place_invalid_latitude_range(self):
        """Test latitude hors bornes (120)"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Mountain Cabin",
            "price": 100.0,
            "latitude": 120.0,
            "longitude": 1.0,
            "owner_id": "dummy-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_place_invalid_latitude_type(self):
        """Test latitude de type string"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Urban Loft",
            "price": 150.0,
            "latitude": "nord",
            "longitude": 1.0,
            "owner_id": "dummy-id"
        })
        self.assertEqual(response.status_code, 400)

    # --- SECTION C: REVIEWS ---
    def test_review_creation_valid(self):
        """Test note valide (5)"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing stay!",
            "rating": 5,
            "user_id": "u-id",
            "place_id": "p-id"
        })
        self.assertEqual(response.status_code, 201)

    def test_review_invalid_rating_range(self):
        """Test note hors bornes (6)"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Bad!",
            "rating": 6,
            "user_id": "u-id",
            "place_id": "p-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_review_invalid_rating_type(self):
        """Test note de type float (4.5) - Attendu Int uniquement"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Good",
            "rating": 4.5,
            "user_id": "u-id",
            "place_id": "p-id"
        })
        self.assertEqual(response.status_code, 400)

    # --- TESTS GLOBAUX ---
    def test_get_non_existent_user(self):
        response = self.client.get('/api/v1/users/id-imaginaire')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()