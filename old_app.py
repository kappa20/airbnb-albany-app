#________pip install streamlit
#Streamlit est un package Python, donc une simple commande pip suffit. Il n’y a pas besoin de configuration supplémentaire. 
#________streamlit run app.py
#Streamlit va ouvrir automatiquement votre navigateur à l’adresse http://localhost:8501. Chaque modification du fichier app.py sera détectée et l’application se rechargera
#_______________________________________________________________________________

import streamlit as st
import pandas as pd

# __________Configuration de la page
st.set_page_config(
    page_title="Airbnb Albany Explorer",
    page_icon="🏠",
    # layout="wide"
)

st.title("Analyse des données Airbnb")
st.header("Chargement et aperçu des données")
st.markdown("""
Ce dataset contient les annonces Airbnb de New York.  
Il comprend des informations comme le prix, le type de logement, le nombre d’avis, etc.
""")
st.divider()
#___________Avec st.title, st.header et st.markdown, 
# on peut facilement organiser le contenu de l’application, comme on le ferait avec du HTML, mais en Python pur.

# Chargement des données (avec mise en cache pour l'exemple)
@st.cache_data
def load_data():
    df = pd.read_csv('listings.csv')
    return df


def get_stats(df):
    """Calcule des statistiques simples pour les tests unitaires."""
    return {
        "total": len(df),
        "mean_price": df['price'].replace('[\$,]', '', regex=True).astype(float).mean() if 'price' in df.columns else 0
    }

df = load_data()
stats = get_stats(df)
st.success(f"Dataset chargé avec succès ! **{stats['total']:,} annonces** et **{df.shape[1]} colonnes**.")
#__________Nous utilisons Pandas pour lire le fichier compressé. Le décorateur @st.cache_data permet de ne charger les données qu’une seule fois, ce qui est très utile pour les gros fichiers comme celui-ci (plusieurs Mo). 

st.dataframe(df.head(10))
# st.table(df.head(5))
#__________st.dataframe() affiche un tableau interactif : on peut trier les colonnes, les redimensionner, et même chercher des valeurs. C’est parfait pour explorer les données. 

# Magic command
df.head(5)
st.write(df.head(5))   
43
# __________Si on écrit juste le nom d’une variable sur une ligne, Streamlit l’affiche automatiquement. C’est ce qu’on appelle les magic commands. Pratique pour des tests rapides


#___________pour l'analyste
st.subheader("3. Affichage dynamique")
rows = st.slider("Nombre de lignes à afficher", min_value=5, max_value=50, value=15, key="slider_rows")
st.dataframe(df.head(rows), use_container_width=True)

if st.checkbox("Afficher les statistiques descriptives"):
    st.write(df.describe())

# st.subheader("4. Types de colonnes")
# st.write(df.dtypes)

# # Expander très pro pour la présentation
# with st.expander("À propos du dataset Airbnb Albany"):
#     st.markdown("""
#     - Données extraites d'Airbnb pour la ville d'**Albany, New York**  
#     - Date de scraping : **07 novembre 2025**  
#     - Colonnes principales : price, room_type, neighbourhood, latitude, longitude, host_name, etc.  
#     - Source : Inside Airbnb (données publiques)
#     """)

# # Bouton de téléchargement
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Télécharger le dataset complet en CSV",
    data=csv,
    file_name="airbnb_albany_listings.csv",
    mime="text/csv"
)

# st.divider()
# st.info("Fin de la partie **Membre 2 – L'Initiateur** !Prêt à passer au Membre 3 pour les visualisations ?")