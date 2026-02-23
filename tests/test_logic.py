import pandas as pd
from app import get_stats

def test_get_stats_calculation():
    """Vérifie que le calcul de la moyenne des prix est correct."""
    # Création d'un mini dataframe de test
    data = {
        'price': ['$100.00', '$200.00', '$300.00']
    }
    df = pd.DataFrame(data)
    
    stats = get_stats(df)
    
    assert stats['total'] == 3
    assert stats['mean_price'] == 200.0

def test_get_stats_empty():
    """Vérifie le comportement avec un dataframe vide."""
    df = pd.DataFrame(columns=['price'])
    stats = get_stats(df)
    assert stats['total'] == 0
