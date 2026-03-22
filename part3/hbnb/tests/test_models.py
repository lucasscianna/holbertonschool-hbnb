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

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_valid_user(self):
        """Un user valide est créé sans erreur"""
        with self.app.app_context():
            user = User(first_name="John", last_name="Doe", email="john@test.com", is_admin=False)
            user.hash_password("password123")
            self.assertEqual(user.first_name, "John")
            self.assertEqual(user.email, "john@test.com")

    def test_invalid_first_name_empty(self):
        """first_name vide lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                User(first_name="", last_name="Doe", email="john@test.com")

    def test_invalid_first_name_too_long(self):
        """first_name > 50 caractères lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                User(first_name="A" * 51, last_name="Doe", email="john@test.com")

    def test_invalid_email_format(self):
        """Email invalide lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                User(first_name="John", last_name="Doe", email="not-an-email")

    def test_password_hashed(self):
        """Le password est bien hashé et différent du texte clair"""
        with self.app.app_context():
            user = User(first_name="John", last_name="Doe", email="john@test.com")
            user.hash_password("password123")
            self.assertNotEqual(user.password, "password123")
            self.assertTrue(user.password.startswith("$2b$"))

    def test_verify_password_correct(self):
        """verify_password retourne True pour le bon mot de passe"""
        with self.app.app_context():
            user = User(first_name="John", last_name="Doe", email="john@test.com")
            user.hash_password("password123")
            self.assertTrue(user.verify_password("password123"))

    def test_verify_password_wrong(self):
        """verify_password retourne False pour un mauvais mot de passe"""
        with self.app.app_context():
            user = User(first_name="John", last_name="Doe", email="john@test.com")
            user.hash_password("password123")
            self.assertFalse(user.verify_password("wrongpassword"))


class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_valid_place(self):
        """Une place valide est créée sans erreur"""
        with self.app.app_context():
            owner = User(first_name="John", last_name="Doe", email="john@test.com")
            place = Place(title="Villa", description="Nice", price=100.0,
                         latitude=10.0, longitude=10.0, owner=owner)
            self.assertEqual(place.title, "Villa")
            self.assertEqual(place.price, 100.0)

    def test_invalid_title_empty(self):
        """Titre vide lève une ValueError"""
        with self.app.app_context():
            owner = User(first_name="John", last_name="Doe", email="john@test.com")
            with self.assertRaises(ValueError):
                Place(title="", description="Nice", price=100.0,
                     latitude=10.0, longitude=10.0, owner=owner)

    def test_invalid_price_negative(self):
        """Prix négatif lève une ValueError"""
        with self.app.app_context():
            owner = User(first_name="John", last_name="Doe", email="john@test.com")
            with self.assertRaises(ValueError):
                Place(title="Villa", description="Nice", price=-5.0,
                     latitude=10.0, longitude=10.0, owner=owner)

    def test_invalid_latitude(self):
        """Latitude hors limites lève une ValueError"""
        with self.app.app_context():
            owner = User(first_name="John", last_name="Doe", email="john@test.com")
            with self.assertRaises(ValueError):
                Place(title="Villa", description="Nice", price=100.0,
                     latitude=200.0, longitude=10.0, owner=owner)

    def test_invalid_longitude(self):
        """Longitude hors limites lève une ValueError"""
        with self.app.app_context():
            owner = User(first_name="John", last_name="Doe", email="john@test.com")
            with self.assertRaises(ValueError):
                Place(title="Villa", description="Nice", price=100.0,
                     latitude=10.0, longitude=500.0, owner=owner)


class TestReviewModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_invalid_rating_too_high(self):
        """Rating > 5 lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                Review(text="Super", rating=6, place_id="x", user_id="y")

    def test_invalid_rating_too_low(self):
        """Rating < 1 lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                Review(text="Super", rating=0, place_id="x", user_id="y")

    def test_invalid_text_empty(self):
        """Texte vide lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                Review(text="", rating=3, place_id="x", user_id="y")


class TestAmenityModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_valid_amenity(self):
        """Une amenity valide est créée sans erreur"""
        with self.app.app_context():
            amenity = Amenity(name="WiFi")
            self.assertEqual(amenity.name, "WiFi")

    def test_invalid_name_empty(self):
        """Nom vide lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                Amenity(name="")

    def test_invalid_name_too_long(self):
        """Nom > 50 caractères lève une ValueError"""
        with self.app.app_context():
            with self.assertRaises(ValueError):
                Amenity(name="A" * 51)

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

if __name__ == '__main__':
    unittest.main(verbosity=2)