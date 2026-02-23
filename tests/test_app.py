from streamlit.testing.v1 import AppTest
import pytest

def test_app_smoke():
    """Vérifie que l'application se lance sans erreur sur la page d'accueil."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert at.title[0].value == "🏠 Airbnb Albany Explorer"

def test_navigation_to_analytics():
    """Vérifie que l'on peut naviguer vers la page Analyses & Graphiques."""
    at = AppTest.from_file("app.py").run()
    
    # Changer de page via le radio de navigation (clé: "nav_radio")
    at.radio(key="nav_radio").set_value("📊 Analyses & Graphiques").run()
    
    assert not at.exception
    assert at.title[0].value == "📊 Visualisations de données"
    # Vérifier la présence des onglets
    assert len(at.tabs) == 3

def test_slider_interaction_homepage():
    """Vérifie que le slider de lignes fonctionne sur la page d'accueil."""
    at = AppTest.from_file("app.py").run()
    
    # Valeur par défaut est 10
    assert at.slider(key="slider_rows").value == 10
    
    # Modifier la valeur
    at.slider(key="slider_rows").set_value(20).run()
    
    # Vérifier que le premier dataframe affiché (aperçu des données) a bien changé
    # at.dataframe[0] est l'aperçu des données
    assert len(at.dataframe[0].value) == 20

def test_search_functionality():
    """Vérifie que la recherche textuelle fonctionne sur la page dédiée."""
    at = AppTest.from_file("app.py").run()
    at.radio(key="nav_radio").set_value("🔍 Recherche Interactive").run()
    
    # Saisir une recherche
    at.text_input[0].set_value("Luxury").run()
    
    # Vérifier qu'un message de succès s'affiche avec le nombre de résultats
    assert any("logements trouvés pour 'Luxury'" in s.value for s in at.success)
