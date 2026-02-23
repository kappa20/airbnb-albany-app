import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Airbnb Albany Explorer",
    page_icon="🏠",
    layout="wide"
)

# --- 2. Data Logic & Caching ---

def clean_price(price):
    """Nettoie la chaîne de caractères du prix pour la convertir en float."""
    if isinstance(price, str):
        return float(price.replace('$', '').replace(',', ''))
    return price

def process_data(df):
    """Nettoie et prépare le dataframe."""
    # Nettoyage du prix
    if 'price' in df.columns:
        df['price'] = df['price'].apply(clean_price)
    
    # Sélection des colonnes pertinentes si elles existent
    cols = ["name", "neighbourhood_cleansed", "room_type", "price",
            "number_of_reviews", "review_scores_rating", "latitude", "longitude", 
            "host_name", "host_is_superhost", "amenities", "accommodates", "bedrooms"]
    df = df[[c for c in cols if c in df.columns]].copy()
    
    return df

@st.cache_data
def load_data(file_path='listings.csv'):
    """Charge les données depuis un CSV avec mise en cache."""
    df = pd.read_csv(file_path, low_memory=False)
    return process_data(df)

def get_stats(df):
    """Calcule des statistiques de résumé pour l'affichage et les tests."""
    if df.empty:
        return {"total": 0, "mean_price": 0.0, "avg_rating": 0.0}
    
    stats = {
        "total": len(df),
        "mean_price": df['price'].mean() if 'price' in df.columns else 0.0,
        "avg_rating": df['review_scores_rating'].mean() if 'review_scores_rating' in df.columns else 0.0
    }
    return stats

# --- 3. Sidebar Navigation & Global Filters ---

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Aller à", ["🏠 Accueil", "🔍 Recherche Interactive", "📊 Analyses & Graphiques", "⚡ Test de Performance"], key="nav_radio")

# Chargement initial des données
try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement de 'listings.csv' : {e}")
    st.stop()

# Filtres globaux dans la barre latérale (appliqués partout sauf sur le test de perf)
if page != "⚡ Test de Performance":
    st.sidebar.divider()
    st.sidebar.header("🎯 Filtres Globaux")
    
    # Filtre par type de logement
    room_types = ["Tous"] + sorted(df_raw["room_type"].dropna().unique().tolist())
    selected_room = st.sidebar.selectbox("Type de logement", room_types)

    # Filtre par quartier
    neighbourhoods = ["Tous"] + sorted(df_raw["neighbourhood_cleansed"].dropna().unique().tolist())
    selected_neighbourhood = st.sidebar.selectbox("Quartier", neighbourhoods)

    # Filtre par prix
    min_p, max_p = int(df_raw["price"].min()), int(df_raw["price"].max())
    price_range = st.sidebar.slider("Budget ($ par nuit)", min_p, min(max_p, 1000), (30, 300))

    # Application des filtres
    df = df_raw.copy()
    if selected_room != "Tous":
        df = df[df["room_type"] == selected_room]
    if selected_neighbourhood != "Tous":
        df = df[df["neighbourhood_cleansed"] == selected_neighbourhood]
    df = df[df["price"].between(price_range[0], price_range[1])]

# --- 4. Contenu des Pages ---

if page == "🏠 Accueil":
    st.title("🏠 Airbnb Albany Explorer")
    st.markdown("""
    Bienvenue dans l'application **Airbnb Albany Explorer** ! 
    Explorez, analysez et visualisez les annonces Airbnb de la ville d'Albany, New York.
    """)
    
    # Métriques clés (Inspiration Membre 5)
    stats = get_stats(df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Annonces", f"{stats['total']:,}")
    col2.metric("Prix Moyen / Nuit", f"${stats['mean_price']:.2f}")
    col3.metric("Note Moyenne", f"{stats['avg_rating']:.2f}/5")
    
    st.divider()
    
    st.header("📋 Aperçu des données")
    rows = st.slider("Nombre de lignes à afficher", 5, 50, 10, key="slider_rows")
    st.dataframe(df.head(rows), use_container_width=True)
    
    if st.checkbox("Afficher les statistiques descriptives"):
        st.write(df.describe())
        
    with st.expander("ℹ️ À propos du Dataset"):
        st.markdown("""
        - **Source** : Inside Airbnb (données publiques).
        - **Localisation** : Albany, New York.
        - **Scraping** : Novembre 2025.
        - **Utilisation** : Ce dashboard combine les travaux de toute l'équipe pour une analyse complète.
        """)
        
    # Bouton de téléchargement (Membre 2)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger les données filtrées (CSV)",
        data=csv,
        file_name="airbnb_albany_filtered.csv",
        mime="text/csv"
    )

elif page == "🔍 Recherche Interactive":
    st.title("🔍 Recherche & Filtres Avancés")
    
    col1, col2 = st.columns(2)
    with col1:
        recherche = st.text_input('Rechercher par nom', placeholder="ex: Luxury, Cozy, Downtown")
        if recherche:
            df_search = df[df['name'].str.contains(recherche, case=False, na=False)]
            st.success(f"🔍 {len(df_search)} logements trouvés pour '{recherche}'")
        else:
            df_search = df

    with col2:
        note_min = st.number_input('Note minimum (0-5)', 0.0, 5.0, 4.0, 0.5)
        df_search = df_search[df_search['review_scores_rating'] >= note_min]
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🎲 Sélection aléatoire")
        if st.button('Piocher un logement au hasard'):
            if not df_search.empty:
                random_item = df_search.sample(1).iloc[0]
                st.info(f"✨ **{random_item['name']}** - {random_item['room_type']} à ${random_item['price']}")
            else:
                st.warning("Aucun logement ne correspond aux critères actuels.")
                
    with col_b:
        st.subheader("👑 Statut Hôte")
        superhost_only = st.toggle("Superhosts uniquement")
        if superhost_only:
            df_search = df_search[df_search['host_is_superhost'] == 't']
            st.write(f"Filtré : {len(df_search)} superhosts restants.")
            
    st.header("Résultats de la recherche")
    st.dataframe(df_search[['name', 'room_type', 'neighbourhood_cleansed', 'price', 'review_scores_rating']].head(20), use_container_width=True)

elif page == "📊 Analyses & Graphiques":
    st.title("📊 Visualisations de données")
    
    tab1, tab2, tab3 = st.tabs(["📉 Distributions", "📈 Relations", "🗺️ Carte"])
    
    with tab1:
        st.subheader("Prix moyen par type de logement")
        price_by_room = df.groupby("room_type")["price"].mean().sort_values(ascending=False)
        st.bar_chart(price_by_room)
        
        st.subheader("Nombre d'annonces par quartier")
        st.bar_chart(df['neighbourhood_cleansed'].value_counts())
        
    with tab2:
        st.subheader("Relation Prix vs Nombre d'avis")
        st.scatter_chart(df, x="price", y="number_of_reviews")
        
        st.subheader("Évolution brute des prix (Liste)")
        st.line_chart(df["price"])
        
    with tab3:
        st.subheader("Localisation géographique des logements")
        if "latitude" in df.columns and "longitude" in df.columns:
            st.map(df[['latitude', 'longitude']].dropna())
        else:
            st.warning("Données de géolocalisation indisponibles.")

elif page == "⚡ Test de Performance":
    st.title("⚡ Démonstration du Caching")
    st.markdown("""
    Cette page illustre l'importance du décorateur `@st.cache_data` pour les applications Streamlit.
    En l'activant, les données lourdes ne sont chargées qu'une seule fois.
    """)
    
    use_cache = st.toggle("Activer la mise en cache (Cache)", value=True)
    
    def simulate_heavy_processing(df):
        time.sleep(1.5) # Simule un traitement long
        return process_data(df)

    def load_no_cache():
        df = pd.read_csv('listings.csv', low_memory=False)
        return simulate_heavy_processing(df)

    @st.cache_data
    def load_with_cache():
        df = pd.read_csv('listings.csv', low_memory=False)
        return simulate_heavy_processing(df)

    start_time = time.time()
    with st.spinner('Chargement des données...'):
        if use_cache:
            data = load_with_cache()
        else:
            data = load_no_cache()
    elapsed = time.time() - start_time
    
    st.write(f"Données chargées en **{elapsed:.4f} secondes**")
    if elapsed < 0.2:
        st.success("Chargement instantané ! (Données récupérées du cache)")
    else:
        st.warning("Chargement lent... (Le script a dû retraiter les données)")
