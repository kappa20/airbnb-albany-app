from streamlit.testing.v1 import AppTest
import pandas as pd
import pytest

def test_app_smoke():
    """Vérifie que l'application se lance sans erreur."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception

def test_data_loading():
    """Vérifie que le succès du chargement s'affiche."""
    at = AppTest.from_file("app.py").run()
    # On cherche le composant st.success
    assert at.success[0].value.startswith("Dataset chargé avec succès")

# def test_slider_interaction():
#     """Vérifie que le slider change le nombre de lignes affichées."""
#     at = AppTest.from_file("app.py").run()
    
#     # On change la valeur du slider (clé : "slider_rows" définie dans app.py)
#     at.slider(key="slider_rows").set_value(25).run()
    
#     # On vérifie que le dataframe affiché contient bien le bon nombre de lignes
#     # Note: st.dataframe est accessible via at.dataframe
#     assert len(at.dataframe[1].value) == 25
