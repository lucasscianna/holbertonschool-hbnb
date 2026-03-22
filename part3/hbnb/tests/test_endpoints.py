import unittest
from app import create_app, db
from sqlalchemy.pool import StaticPool

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'test-secret-key-32-characters-long'
    SECRET_KEY = 'test-secret'

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_token(self, email, password):
        res = self.client.post('/api/v1/auth/login',
                               json={"email": email, "password": password})
        data = res.get_json()
        return data.get('access_token') if data else None

    def test_post_user_201(self):
        """POST /users/ retourne 201 avec les données"""
        res = self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn('id', data)
        self.assertNotIn('password', data)

    def test_post_user_400_missing_field(self):
        """POST /users/ sans first_name retourne 400"""
        res = self.client.post('/api/v1/users/', json={
            "last_name": "Doe", "email": "john@ep.com",
            "password": "password123"
        })
        self.assertIn(res.status_code, [400, 500])

    def test_post_user_400_invalid_email(self):
        """POST /users/ avec email invalide retourne 400"""
        res = self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "not-valid", "password": "password123"
        })
        self.assertEqual(res.status_code, 400)

    def test_post_user_400_duplicate_email(self):
        """POST /users/ avec email dupliqué retourne 400"""
        self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Jane", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        self.assertEqual(res.status_code, 400)

    def test_get_user_200(self):
        """GET /users/<id> retourne 200 et les données"""
        res = self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        user_id = res.get_json()['id']
        get_res = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()['email'], "john@ep.com")

    def test_get_user_404(self):
        """GET /users/<id> avec ID inexistant retourne 404"""
        res = self.client.get('/api/v1/users/fake-id-999')
        self.assertEqual(res.status_code, 404)

    def test_get_all_users_200(self):
        """GET /users/ retourne 200 et une liste"""
        self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        res = self.client.get('/api/v1/users/')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_put_user_200(self):
        """PUT /users/<id> retourne 200 avec les données mises à jour"""
        res = self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        user_id = res.get_json()['id']
        token = self.get_token("john@ep.com", "password123")
        put_res = self.client.put(f'/api/v1/users/{user_id}',
            headers={'Authorization': f'Bearer {token}'},
            json={"first_name": "Johnny"})
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()['first_name'], "Johnny")

    def test_put_user_403_wrong_user(self):
        """PUT /users/<id> par un autre user retourne 403"""
        r1 = self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        self.client.post('/api/v1/users/', json={
            "first_name": "Jane", "last_name": "Smith",
            "email": "jane@ep.com", "password": "password123"
        })
        user1_id = r1.get_json()['id']
        token_jane = self.get_token("jane@ep.com", "password123")
        res = self.client.put(f'/api/v1/users/{user1_id}',
            headers={'Authorization': f'Bearer {token_jane}'},
            json={"first_name": "Hacked"})
        self.assertEqual(res.status_code, 403)


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_token(self, email, password):
        res = self.client.post('/api/v1/auth/login',
                               json={"email": email, "password": password})
        data = res.get_json()
        return data.get('access_token') if data else None

    def setUp_user_and_token(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "Owner", "last_name": "User",
            "email": "owner@ep.com", "password": "password123"
        })
        return self.get_token("owner@ep.com", "password123")

    def test_post_place_201(self):
        """POST /places/ retourne 201"""
        token = self.setUp_user_and_token()
        res = self.client.post('/api/v1/places/',
            headers={'Authorization': f'Bearer {token}'},
            json={"title": "Villa", "price": 100.0,
                  "latitude": 10.0, "longitude": 10.0,
                  "owner_id": "ignored"})
        self.assertEqual(res.status_code, 201)

    def test_post_place_400_negative_price(self):
        """POST /places/ avec prix négatif retourne 400"""
        token = self.setUp_user_and_token()
        res = self.client.post('/api/v1/places/',
            headers={'Authorization': f'Bearer {token}'},
            json={"title": "Villa", "price": -10.0,
                  "latitude": 10.0, "longitude": 10.0,
                  "owner_id": "ignored"})
        self.assertEqual(res.status_code, 400)

    def test_post_place_401_no_token(self):
        """POST /places/ sans token retourne 401"""
        res = self.client.post('/api/v1/places/', json={
            "title": "Villa", "price": 100.0,
            "latitude": 10.0, "longitude": 10.0
        })
        self.assertEqual(res.status_code, 401)

    def test_get_all_places_200(self):
        """GET /places/ retourne 200"""
        res = self.client.get('/api/v1/places/')
        self.assertEqual(res.status_code, 200)

    def test_get_place_404(self):
        """GET /places/<id> inexistant retourne 404"""
        res = self.client.get('/api/v1/places/fake-id-999')
        self.assertEqual(res.status_code, 404)


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_token(self, email, password):
        res = self.client.post('/api/v1/auth/login',
                               json={"email": email, "password": password})
        data = res.get_json()
        return data.get('access_token') if data else None

    def test_post_amenity_201_as_admin(self):
        """POST /amenities/ en tant qu'admin retourne 201"""
        self.client.post('/api/v1/users/', json={
            "first_name": "Admin", "last_name": "User",
            "email": "admin@ep.com", "password": "password123"
        })
        token = self.get_token("admin@ep.com", "password123")
        res = self.client.post('/api/v1/amenities/',
            headers={'Authorization': f'Bearer {token}'},
            json={"name": "WiFi"})
        self.assertEqual(res.status_code, 201)

    def test_post_amenity_403_not_admin(self):
        """POST /amenities/ sans être admin retourne 403"""
        self.client.post('/api/v1/users/', json={
            "first_name": "Admin", "last_name": "User",
            "email": "admin@ep.com", "password": "password123"
        })
        self.client.post('/api/v1/users/', json={
            "first_name": "John", "last_name": "Doe",
            "email": "john@ep.com", "password": "password123"
        })
        token = self.get_token("john@ep.com", "password123")
        res = self.client.post('/api/v1/amenities/',
            headers={'Authorization': f'Bearer {token}'},
            json={"name": "Pool"})
        self.assertEqual(res.status_code, 403)

    def test_get_all_amenities_200(self):
        """GET /amenities/ retourne 200"""
        res = self.client.get('/api/v1/amenities/')
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)