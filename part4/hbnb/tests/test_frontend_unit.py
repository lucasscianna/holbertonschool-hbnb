import unittest
import os
import re

# Chemin vers le dossier racine du frontend (relatif à part4/hbnb/tests)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class TestFrontendUnit(unittest.TestCase):
    
    def test_required_html_files_exist(self):
        """Vérifie la présence des fichiers HTML requis (Structure Sanity Check)"""
        expected_files = ['index.html', 'login.html', 'place.html', 'add_review.html']
        for html_file in expected_files:
            file_path = os.path.join(FRONTEND_DIR, html_file)
            self.assertTrue(os.path.exists(file_path), f"Fichier attendu manquant: {html_file}")

    def test_required_js_scripts_exist(self):
        """Vérifie la présence de l'architecture JavaScript"""
        expected_js_files = [
            'scripts.js',
            'scripts/index.js',
            'scripts/login.js',
            'scripts/place.js',
            'scripts/review.js'
        ]
        for js_file in expected_js_files:
            file_path = os.path.join(FRONTEND_DIR, js_file)
            self.assertTrue(os.path.exists(file_path), f"Script manquant: {js_file}")

    def test_css_file_exists(self):
        """Vérifie l'existence du design system central (styles.css)"""
        file_path = os.path.join(FRONTEND_DIR, 'styles.css')
        self.assertTrue(os.path.exists(file_path), "Fichier styles.css manquant")

    def test_html_includes_main_script(self):
        """Vérifie que les fichiers HTML importent bien les scripts de base"""
        expected_files = ['index.html', 'login.html', 'place.html']
        for html_file in expected_files:
            file_path = os.path.join(FRONTEND_DIR, html_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertIn('scripts.js', content, f"{html_file} doit inclure scripts.js")

    def test_index_is_semantic(self):
        """Vérifie la sémantique de base de l'index"""
        index_path = os.path.join(FRONTEND_DIR, 'index.html')
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('<header>', content)
            self.assertIn('<main>', content)
            self.assertIn('<footer>', content)

if __name__ == '__main__':
    unittest.main()
