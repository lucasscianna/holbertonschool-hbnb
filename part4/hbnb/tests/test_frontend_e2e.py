import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Ce test nécessite que :
# 1. L'API backend flask tourne sur http://127.0.0.1:5000 (python run.py)
# 2. Les fichiers frontends soient servis (par ex: via un live server ou directement ouverts dans chrome si le CORS file:// le permet)
# Pour une meilleure fiabilité, on suppose ici que le frontend est servi via http://127.0.0.1:8000

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:8000")

class TestFrontendE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Exécution sans interface graphique
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        try:
            cls.driver = webdriver.Chrome(options=options)
            cls.driver.implicitly_wait(3)
        except Exception as e:
            cls.skipTest(cls, f"Selenium Chrome Webdriver non disponible: {e}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()

    def setUp(self):
        # Assurez-vous d'avoir une session vierge pour chaque test
        self.driver.delete_all_cookies()

    def test_index_unauthenticated_shows_login_link(self):
        """Vérifie que la page d'accueil affiche 'Login' si non connecté"""
        self.driver.get(f"{FRONTEND_URL}/index.html")
        login_link = self.driver.find_element(By.ID, "login-link")
        self.assertTrue(login_link.is_displayed())
        self.assertEqual(login_link.text, "Login")

    def test_login_flow(self):
        """Vérifie le flux de connexion jusqu'à la redirection et bouton de déconnexion"""
        self.driver.get(f"{FRONTEND_URL}/login.html")
        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button.submit-button")

        # Remplir (on suppose admin existant ou erreur gérée)
        email_input.send_keys("admin@admin.com")
        password_input.send_keys("password123")
        submit_btn.click()

        # Attendre la redirection vers index
        WebDriverWait(self.driver, 5).until(EC.url_contains("index.html"))
        
        # Vérification qu'on est bien connecté (login caché)
        login_link = self.driver.find_element(By.ID, "login-link")
        # Selon index.js on cache le bloc de login ou on change le texte "Log Out" (dans scripts.js)
        # Mais dans index.js actuel on le check via 'display: none'
        self.assertFalse(login_link.is_displayed())

    def test_add_review_redirects_if_unauthenticated(self):
        """Tester que l'accès à add_review.html sans token renvoie à l'index"""
        # Note: add_review.html a été codé différemment ou fusionné dans place.html dans the "Simple Web Client"
        # Mais puisqu'il y a un fichier add_review.html, on peut le tester
        self.driver.get(f"{FRONTEND_URL}/add_review.html")
        WebDriverWait(self.driver, 2).until(EC.url_contains("index.html"))
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
