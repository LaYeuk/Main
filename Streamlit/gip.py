import streamlit as st
import pandas as pd

#Mise en page
#Suppression des marges

st.markdown("""
        <style>
            .block-container {
                padding-top: 3rem;
                padding-bottom: 0rem;
                padding-left: 0rem !important;
                padding-right: 0rem !important;
            }
            .main {
                padding-left: 0rem !important;
                padding-right: 0rem !important;
            }
        </style>
        """, unsafe_allow_html=True)



#ajout des colonnes
col1, col2= st.columns(2)

with col1:
    st.image("Streamlit/Identité visuelle - Logo GIP (ID 41903).svg")


with col2:
    # Titre principal de la page
    st.title("Dashboard GIP")




# Titre de l'application
st.title("Tableau de saisie des primes")

# Demander à l'utilisateur de renseigner le nombre d'années (colonnes)
nombre_annees = st.number_input("Nombre d'années :", min_value=1, step=1, value=3)

# Colonnes du tableau (noms des années dynamiques)
colonnes = [f"Année {i+1}" for i in range(int(nombre_annees))]

# Lignes fixes pour les catégories
lignes = ["Prime totale", "Prime admin", "Prime risque"]

# Créer un DataFrame vide (valeurs initialisées à 0)
df = pd.DataFrame(0, index=lignes, columns=colonnes)

# Permettre à l'utilisateur de modifier les valeurs dans le tableau interactif
edited_df = st.experimental_data_editor(df, num_rows="fixed", use_container_width=True)

# Optionnel : Afficher le tableau après édition
st.write("Tableau complété par l'utilisateur :")
st.dataframe(edited_df)
