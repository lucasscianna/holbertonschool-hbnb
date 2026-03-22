import unittest
from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
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

class TestSQLAlchemyRepository(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _make_user(self, email="test@test.com"):
        user = User(first_name="John", last_name="Doe", email=email, is_admin=False)
        user.hash_password("password123")
        return user

    def test_add_and_get(self):
        """add() puis get() retourne le bon objet"""
        with self.app.app_context():
            repo = UserRepository()
            user = self._make_user()
            repo.add(user)
            fetched = repo.get(user.id)
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched.email, "test@test.com")

    def test_get_nonexistent(self):
        """get() retourne None pour un ID inexistant"""
        with self.app.app_context():
            repo = UserRepository()
            result = repo.get("fake-id-000")
            self.assertIsNone(result)

    def test_get_all(self):
        """get_all() retourne tous les objets"""
        with self.app.app_context():
            repo = UserRepository()
            repo.add(self._make_user("a@test.com"))
            repo.add(self._make_user("b@test.com"))
            all_users = repo.get_all()
            self.assertEqual(len(all_users), 2)

    def test_update(self):
        """update() modifie bien l'attribut en base"""
        with self.app.app_context():
            repo = UserRepository()
            user = self._make_user()
            repo.add(user)
            repo.update(user.id, {"first_name": "Jane"})
            updated = repo.get(user.id)
            self.assertEqual(updated.first_name, "Jane")

    def test_delete(self):
        """delete() supprime bien l'objet"""
        with self.app.app_context():
            repo = UserRepository()
            user = self._make_user()
            repo.add(user)
            repo.delete(user.id)
            self.assertIsNone(repo.get(user.id))

    def test_get_by_attribute(self):
        """get_by_attribute() retrouve un objet par attribut"""
        with self.app.app_context():
            repo = UserRepository()
            user = self._make_user("unique@test.com")
            repo.add(user)
            found = repo.get_by_attribute("email", "unique@test.com")
            self.assertIsNotNone(found)
            self.assertEqual(found.email, "unique@test.com")


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_user_by_email_found(self):
        """get_user_by_email() retourne le bon user"""
        with self.app.app_context():
            repo = UserRepository()
            user = User(first_name="John", last_name="Doe",
                       email="find@test.com", is_admin=False)
            user.hash_password("password123")
            repo.add(user)
            found = repo.get_user_by_email("find@test.com")
            self.assertIsNotNone(found)
            self.assertEqual(found.email, "find@test.com")

    def test_get_user_by_email_not_found(self):
        """get_user_by_email() retourne None si email inconnu"""
        with self.app.app_context():
            repo = UserRepository()
            result = repo.get_user_by_email("nobody@test.com")
            self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main(verbosity=2)