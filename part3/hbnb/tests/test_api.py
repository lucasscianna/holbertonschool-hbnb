import unittest
from app import create_app

class TestHBnBAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Données pour les tests de sécurité
        self.user_john = {
            "first_name": "John", "last_name": "Doe",
            "email": "john.doe@hbnb.com", "password": "password123"
        }
        self.user_jane = {
            "first_name": "Jane", "last_name": "Smith",
            "email": "jane.smith@hbnb.com", "password": "password123"
        }

    def get_token(self, email, password):
        """Méthode utilitaire pour simuler un login et récupérer un JWT"""
        response = self.client.post('/api/v1/auth/login', json={
            "email": email, "password": password
        })
        return response.get_json().get('access_token')

    # --- TES TESTS ORIGINAUX (CONSERVÉS AVEC MODIFICATION AUTH) ---

    def test_user_creation_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@hbnb.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)

    def test_user_creation_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice", "last_name": "Smith", "email": "mauvais-format"
        })
        self.assertEqual(response.status_code, 400)

    def test_place_invalid_price(self):
        # Ajout de l'utilisateur et du token pour éviter la 401
        self.client.post('/api/v1/users/', json=self.user_john)
        token = self.get_token(self.user_john['email'], "password123")
        headers = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/api/v1/places/', headers=headers, json={
            "title": "Beach House", "price": -10.0,
            "latitude": 45.0, "longitude": 1.0
        })
        self.assertEqual(response.status_code, 400)

    def test_review_invalid_rating(self):
        # 1. On crée l'utilisateur et on récupère son token
        self.client.post('/api/v1/users/', json=self.user_john)
        token = self.get_token(self.user_john['email'], "password123")
        headers = {'Authorization': f'Bearer {token}'}

        # 2. On crée une VRAIE villa pour que l'ID soit valide (évite le 404)
        place_resp = self.client.post('/api/v1/places/', headers=headers, json={
            "title": "Test Place", "description": "Temp", "price": 100.0,
            "latitude": 48.8, "longitude": 2.3
        })
        real_place_id = place_resp.get_json().get('id')

        # 3. On teste la note invalide (7) sur cette VRAIE villa
        response = self.client.post('/api/v1/reviews/', headers=headers, json={
            "text": "Super!", 
            "rating": 7, 
            "place_id": real_place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_non_existent_user(self):
        response = self.client.get('/api/v1/users/id-imaginaire')
        self.assertEqual(response.status_code, 404)

    # --- NOUVEAUX TESTS AJOUTÉS (TASK 3 : SÉCURITÉ) ---

    def test_authorization_logic(self):
        """Vérifie que les permissions et les règles métier sont respectées"""
        # 1. Inscription et Login
        self.client.post('/api/v1/users/', json=self.user_john)
        self.client.post('/api/v1/users/', json=self.user_jane)
        
        token_john = self.get_token(self.user_john['email'], "password123")
        token_jane = self.get_token(self.user_jane['email'], "password123")

        # 2. John crée une place
        headers_john = {'Authorization': f'Bearer {token_john}'}
        place_resp = self.client.post('/api/v1/places/', headers=headers_john, json={
            "title": "Villa John", "description": "Privée", "price": 100.0,
            "latitude": 48.8, "longitude": 2.3
        })
        place_id = place_resp.get_json().get('id')
        user_id_john = place_resp.get_json().get('owner_id')

        # TEST : Jane essaie de modifier la place de John (Attendu: 403)
        headers_jane = {'Authorization': f'Bearer {token_jane}'}
        resp_put = self.client.put(f'/api/v1/places/{place_id}', headers=headers_jane, json={
            "title": "Piratage"
        })
        self.assertEqual(resp_put.status_code, 403)

        # TEST : John tente de se noter lui-même (Attendu: 400)
        resp_rev = self.client.post('/api/v1/reviews/', headers=headers_john, json={
            "place_id": place_id, "text": "Je suis génial", "rating": 5
        })
        self.assertEqual(resp_rev.status_code, 400)

        # TEST : Modification d'email interdite (Attendu: 400)
        resp_email = self.client.put(f'/api/v1/users/{user_id_john}', 
                                    headers=headers_john, json={"email": "hacker@hbnb.com"})
        self.assertEqual(resp_email.status_code, 400)

if __name__ == '__main__':
    unittest.main()