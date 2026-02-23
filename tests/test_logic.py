import pandas as pd
import pytest
from app import get_stats, clean_price, process_data

def test_clean_price():
    """Vérifie que le nettoyage des prix fonctionne correctement."""
    assert clean_price("$1,200.50") == 1200.50
    assert clean_price("100") == 100.0
    assert clean_price(75.0) == 75.0

def test_get_stats_calculation():
    """Vérifie que le calcul des statistiques est correct."""
    data = {
        'price': [100.0, 200.0, 300.0],
        'review_scores_rating': [4.0, 4.5, 5.0]
    }
    df = pd.DataFrame(data)
    
    stats = get_stats(df)
    
    assert stats['total'] == 3
    assert stats['mean_price'] == 200.0
    assert stats['avg_rating'] == 4.5

def test_get_stats_empty():
    """Vérifie le comportement avec un dataframe vide."""
    df = pd.DataFrame(columns=['price', 'review_scores_rating'])
    stats = get_stats(df)
    assert stats['total'] == 0
    assert stats['mean_price'] == 0.0
    assert stats['avg_rating'] == 0.0

def test_process_data_integration():
    """Vérifie le traitement global d'un dataframe brut."""
    data = {
        'name': ['Test'],
        'price': ['$100.00'],
        'neighbourhood_cleansed': ['Albany'],
        'room_type': ['Private room'],
        'unknown_col': ['Ignore me']
    }
    df_raw = pd.DataFrame(data)
    df_processed = process_data(df_raw)
    
    assert 'price' in df_processed.columns
    assert df_processed['price'].iloc[0] == 100.0
    assert 'unknown_col' not in df_processed.columns
    assert 'name' in df_processed.columns
