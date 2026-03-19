import unittest
import time
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

class TestHBnBAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        ts = int(time.time() * 1000)
        self.email_admin = f"admin_{ts}@hbnb.com"
        self.email_john  = f"john_{ts}@hbnb.com"
        self.email_jane  = f"jane_{ts}@hbnb.com"

        self.user_admin = {
            "first_name": "Admin", "last_name": "HBnB",
            "email": self.email_admin, "password": "adminpassword"
        }
        self.user_john = {
            "first_name": "John", "last_name": "Doe",
            "email": self.email_john, "password": "password123"
        }
        self.user_jane = {
            "first_name": "Jane", "last_name": "Smith",
            "email": self.email_jane, "password": "password123"
        }

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_token(self, email, password):
        response = self.client.post('/api/v1/auth/login', json={
            "email": email, "password": password
        })
        data = response.get_json()
        return data.get('access_token') if data else None

    def test_user_persisted_in_db(self):
        """T6 — Le user est bien sauvegardé en base SQLAlchemy"""
        res = self.client.post('/api/v1/users/', json=self.user_john)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['email'], self.email_john)

    def test_password_not_returned(self):
        """T6 — Le password hashé ne doit jamais apparaître dans la réponse"""
        res = self.client.post('/api/v1/users/', json=self.user_john)
        data = res.get_json()
        self.assertNotIn('password', data)

    def test_duplicate_email_rejected(self):
        """T6 — Un email déjà utilisé doit retourner 400"""
        self.client.post('/api/v1/users/', json=self.user_john)
        res2 = self.client.post('/api/v1/users/', json=self.user_john)
        self.assertEqual(res2.status_code, 400)

    def test_get_user_by_id(self):
        """T6 — Récupérer un user par son ID depuis la DB"""
        res = self.client.post('/api/v1/users/', json=self.user_john)
        user_id = res.get_json().get('id')
        get_res = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()['email'], self.email_john)

    def test_get_all_users(self):
        """T6 — GET /users/ retourne bien la liste depuis la DB"""
        self.client.post('/api/v1/users/', json=self.user_john)
        self.client.post('/api/v1/users/', json=self.user_jane)
        res = self.client.get('/api/v1/users/')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.get_json()), 2)

    def test_update_user(self):
        """T6 — Mise à jour d'un user persistée en base"""
        res = self.client.post('/api/v1/users/', json=self.user_john)
        user_id = res.get_json().get('id')
        token = self.get_token(self.email_john, "password123")

        put_res = self.client.put(
            f'/api/v1/users/{user_id}',
            headers={'Authorization': f'Bearer {token}'},
            json={"first_name": "Johnny"}
        )
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()['first_name'], 'Johnny')

    def test_first_user_is_admin(self):
        """T6 — Le premier user créé reçoit is_admin=True"""
        res = self.client.post('/api/v1/users/', json=self.user_admin)
        self.assertEqual(res.status_code, 201)
        token = self.get_token(self.email_admin, "adminpassword")
        res_amenity = self.client.post(
            '/api/v1/amenities/',
            headers={'Authorization': f'Bearer {token}'},
            json={"name": "Pool"}
        )
        self.assertEqual(res_amenity.status_code, 201)

    def test_user_creation_valid(self):
        """Vérifie la création d'un utilisateur (1er user = admin auto)"""
        response = self.client.post('/api/v1/users/', json=self.user_admin)
        self.assertEqual(response.status_code, 201)

    def test_user_creation_invalid_email(self):
        """Vérifie le rejet d'un format email invalide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice", "last_name": "Smith", "email": "not-an-email",
            "password": "password123"
        })
        self.assertIn(response.status_code, [400, 401, 403])

    def test_get_non_existent_user(self):
        """Vérifie le retour 404 pour un ID inconnu"""
        response = self.client.get('/api/v1/users/non-existent-id-123')
        self.assertEqual(response.status_code, 404)

    def test_place_invalid_price(self):
        """Vérifie que le prix négatif est rejeté"""
        self.client.post('/api/v1/users/', json=self.user_john)
        token = self.get_token(self.email_john, "password123")
        headers = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/api/v1/places/', headers=headers, json={
            "title": "Cheap Hut", "price": -5.0,
            "latitude": 10.0, "longitude": 10.0, "owner_id": "ignored"
        })
        self.assertEqual(response.status_code, 400)

    def test_review_invalid_rating(self):
        """Vérifie que la note doit être entre 1 et 5"""
        self.client.post('/api/v1/users/', json=self.user_john)
        token = self.get_token(self.email_john, "password123")
        headers = {'Authorization': f'Bearer {token}'}

        p_res = self.client.post('/api/v1/places/', headers=headers, json={
            "title": "Villa", "price": 100.0,
            "latitude": 1.0, "longitude": 1.0, "owner_id": "ignored"
        })
        p_id = p_res.get_json().get('id')

        response = self.client.post('/api/v1/reviews/', headers=headers, json={
            "text": "Too good to be true", "rating": 7,
            "place_id": p_id, "user_id": "ignored"
        })
        self.assertEqual(response.status_code, 400)

    def test_authorization_logic(self):
        """Vérifie que Jane ne peut pas modifier la place de John"""
        self.client.post('/api/v1/users/', json=self.user_john)
        self.client.post('/api/v1/users/', json=self.user_jane)

        t_john = self.get_token(self.email_john, "password123")
        t_jane = self.get_token(self.email_jane, "password123")

        p_resp = self.client.post('/api/v1/places/',
            headers={'Authorization': f'Bearer {t_john}'}, json={
                "title": "John's House", "price": 100.0,
                "latitude": 1.0, "longitude": 1.0, "owner_id": "ignored"
            })
        p_id = p_resp.get_json().get('id')

        resp_put = self.client.put(f'/api/v1/places/{p_id}',
            headers={'Authorization': f'Bearer {t_jane}'}, json={
                "title": "Jane was here"
            })
        self.assertEqual(resp_put.status_code, 404)

    def test_admin_privileges(self):
        """Vérifie que seul l'admin peut créer une Amenity"""
        self.client.post('/api/v1/users/', json=self.user_admin)
        self.client.post('/api/v1/users/', json=self.user_john)

        t_john  = self.get_token(self.email_john, "password123")
        t_admin = self.get_token(self.email_admin, "adminpassword")

        res_fail = self.client.post('/api/v1/amenities/',
            headers={'Authorization': f'Bearer {t_john}'},
            json={"name": "Pool"})
        self.assertEqual(res_fail.status_code, 403)

        res_ok = self.client.post('/api/v1/amenities/',
            headers={'Authorization': f'Bearer {t_admin}'},
            json={"name": "WiFi"})
        self.assertEqual(res_ok.status_code, 201)


if __name__ == '__main__':
    unittest.main(verbosity=2)