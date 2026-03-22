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

class TestUserFacade(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user_valid(self):
        """create_user() crée et retourne un user valide"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            user = facade.create_user({
                "first_name": "John", "last_name": "Doe",
                "email": "john@facade.com", "password": "password123"
            })
            self.assertIsNotNone(user.id)
            self.assertEqual(user.email, "john@facade.com")

    def test_create_user_first_is_admin(self):
        """Le premier user créé est automatiquement admin"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            user = facade.create_user({
                "first_name": "Admin", "last_name": "User",
                "email": "admin@facade.com", "password": "password123"
            })
            self.assertTrue(user.is_admin)

    def test_create_user_second_not_admin(self):
        """Le deuxième user n'est pas admin"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            facade.create_user({
                "first_name": "Admin", "last_name": "User",
                "email": "admin@facade.com", "password": "password123"
            })
            user2 = facade.create_user({
                "first_name": "John", "last_name": "Doe",
                "email": "john@facade.com", "password": "password123"
            })
            self.assertFalse(user2.is_admin)

    def test_create_user_duplicate_email(self):
        """Email dupliqué lève une ValueError"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            facade.create_user({
                "first_name": "John", "last_name": "Doe",
                "email": "john@facade.com", "password": "password123"
            })
            with self.assertRaises(ValueError):
                facade.create_user({
                    "first_name": "Jane", "last_name": "Doe",
                    "email": "john@facade.com", "password": "password123"
                })

    def test_create_user_invalid_email(self):
        """Email invalide lève une ValueError"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            with self.assertRaises(ValueError):
                facade.create_user({
                    "first_name": "John", "last_name": "Doe",
                    "email": "not-an-email", "password": "password123"
                })

    def test_get_user(self):
        """get_user() retourne le bon user"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            user = facade.create_user({
                "first_name": "John", "last_name": "Doe",
                "email": "john@facade.com", "password": "password123"
            })
            fetched = facade.get_user(user.id)
            self.assertEqual(fetched.id, user.id)

    def test_get_user_by_email(self):
        """get_user_by_email() retrouve un user par email"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            facade.create_user({
                "first_name": "John", "last_name": "Doe",
                "email": "john@facade.com", "password": "password123"
            })
            found = facade.get_user_by_email("john@facade.com")
            self.assertIsNotNone(found)

    def test_get_all_users(self):
        """get_all_users() retourne tous les users"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            facade.create_user({
                "first_name": "John", "last_name": "Doe",
                "email": "john@facade.com", "password": "password123"
            })
            facade.create_user({
                "first_name": "Jane", "last_name": "Smith",
                "email": "jane@facade.com", "password": "password123"
            })
            users = facade.get_all_users()
            self.assertEqual(len(users), 2)

    def test_update_user(self):
        """update_user() met à jour les attributs"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            user = facade.create_user({
                "first_name": "John", "last_name": "Doe",
                "email": "john@facade.com", "password": "password123"
            })
            updated = facade.update_user(user.id, {"first_name": "Johnny"})
            self.assertEqual(updated.first_name, "Johnny")

    def test_update_user_not_found(self):
        """update_user() retourne None si user inexistant"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            result = facade.update_user("fake-id", {"first_name": "Ghost"})
            self.assertIsNone(result)


class TestPlaceFacade(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _create_owner(self, facade):
        return facade.create_user({
            "first_name": "Owner", "last_name": "User",
            "email": "owner@facade.com", "password": "password123"
        })

    def test_create_place_valid(self):
        """create_place() crée une place valide"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            owner = self._create_owner(facade)
            place = facade.create_place({
                "title": "Villa", "description": "Nice",
                "price": 100.0, "latitude": 10.0,
                "longitude": 10.0, "owner_id": owner.id
            })
            self.assertEqual(place.title, "Villa")
            self.assertEqual(place.price, 100.0)
            self.assertEqual(place.owner.id, owner.id)

    def test_create_place_invalid_price(self):
        """Prix négatif lève une ValueError"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            owner = self._create_owner(facade)
            with self.assertRaises(ValueError):
                facade.create_place({
                    "title": "Villa", "price": -10.0,
                    "latitude": 10.0, "longitude": 10.0,
                    "owner_id": owner.id
                })

    def test_create_place_owner_not_found(self):
        """Owner inexistant lève une ValueError"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            with self.assertRaises(ValueError):
                facade.create_place({
                    "title": "Villa", "price": 100.0,
                    "latitude": 10.0, "longitude": 10.0,
                    "owner_id": "fake-owner-id"
                })

    def test_get_place(self):
        """get_place() retourne la bonne place"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            owner = self._create_owner(facade)
            place = facade.create_place({
                "title": "Villa", "price": 100.0,
                "latitude": 10.0, "longitude": 10.0,
                "owner_id": owner.id
            })
            fetched = facade.get_place(place.id)
            self.assertEqual(fetched.id, place.id)


class TestAmenityFacade(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_amenity_valid(self):
        """create_amenity() crée une amenity valide"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            amenity = facade.create_amenity({"name": "WiFi"})
            self.assertEqual(amenity.name, "WiFi")

    def test_create_amenity_empty_name(self):
        """Nom vide lève une ValueError"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            with self.assertRaises(ValueError):
                facade.create_amenity({"name": ""})

    def test_get_all_amenities(self):
        """get_all_amenities() retourne toutes les amenities"""
        with self.app.app_context():
            from app.services.facade import HBnBFacade
            facade = HBnBFacade()
            a1 = facade.create_amenity({"name": "WiFi"})
            a2 = facade.create_amenity({"name": "Pool"})
            self.assertEqual(a1.name, "WiFi")
            self.assertEqual(a2.name, "Pool")
            amenities = facade.get_all_amenities()
            self.assertGreaterEqual(len(amenities), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)