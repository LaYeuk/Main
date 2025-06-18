import pandas as pd
import pyodbc
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

# Configuration de la connexion à la base de données
connection_string = (
    "DRIVER={Progress OpenEdge 12.2 Driver};"
    "HOSTNAME=10.0.0.4;"  # Adresse du serveur
    "PORT=12508;"  # Port
    "DATABASE=Concept;"  # Nom de la base
    "UID=gip;"  # Nom d'utilisateur
    "PWD=Gip2025!;"  # Mot de passe
)

# Widgets Streamlit pour récupérer les entrées utilisateur
st.sidebar.header("Filtres de recherche")

portf_id = st.sidebar.text_input("Entrez le PortfId :", value="112001")
valuation_date = st.sidebar.date_input("Entrez la ValuationDate :")

try:
    # Vérification des entrées utilisateur
    if portf_id and valuation_date:
        # Établir la connexion
        with pyodbc.connect(connection_string) as conn:
            # Construction de la requête SQL avec les paramètres
            query = f"""
            SELECT LineCode, LineLabel, InterestRate, MaturityDate, Currency, Quantity, 
       PurchasePrice, PurchaseValue,PurchaseValueRef, MarketPrice, MarketValue, MarketValueRef, LineTotalRef

            FROM PUB.cpsValuatLine
            WHERE PortfId = ?
              AND PriceDate = ?
            """

            # Exécuter la requête avec substitution des paramètres
            df = pd.read_sql(query, conn, params=[portf_id, valuation_date])

            # Vérification des résultats de la requête
            if not df.empty:
                # Afficher les données dans Streamlit
                st.markdown(f"<p style='font-size:15px;'>Portfolio Code : {portf_id}<br>Date : {valuation_date}</p>",unsafe_allow_html=True)


                st.dataframe(df)
            else:
                st.warning(f"Aucune ligne trouvée pour PortfId = {portf_id} et ValuationDate = {valuation_date}.")

except pyodbc.Error as e:
    # Message d'erreur pour les problèmes liés à la connexion ou à l'exécution de la requête
    st.error(f"Erreur ODBC : {e}")
except Exception as ex:
    # Message d'erreur pour toute autre exception
    st.error(f"Erreur générale : {ex}")


# Créer les données pour le tableau "Nom" et "Metrics"
metrics_data = {
    "Nom": [

        "Rendement annualisé",
        "Volatilité annualisé",
        "Max Drawdown",

        "Beta"
    ],
    "Metrics": [

        "7.62%",
        "5.2%",
        "7.8%",

        "0.93%"
    ]
}

# Créer un DataFrame à partir des données
metrics_df = pd.DataFrame(metrics_data)

# Ajouter un sous-titre puis afficher le tableau
st.markdown(
    f"<p style='font-size:15px; font-weight:600;'>Metrics du portefeuille : {portf_id}</p>",
    unsafe_allow_html=True
)



##########Chart

# Convertir les Metrics en valeurs numériques et normaliser (élimination du symbole % ou du signe -)
metrics_values = [float(value.strip("%")) for value in metrics_data["Metrics"]]

# Création des labels et des angles pour le radar chart
labels = metrics_data["Nom"]
num_vars = len(labels)

# Angles pour chaque axe
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Fermer le graphe (assurer la fermeture du cercle dans le spider chart)
values = metrics_values + metrics_values[:1]
angles += angles[:1]

# Créer le graphe radar
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Dessiner l'araignée
ax.fill(angles, values, color='skyblue', alpha=0.5)
ax.plot(angles, values, color='blue', linewidth=2)

# Ajouter les labels de chaque axe
ax.set_yticks([])
ax.set_thetagrids(np.degrees(angles[:-1]), labels)



# Affichage côte à côte avec deux colonnes
col1, col2 = st.columns(2)

with col1:

    st.dataframe(metrics_df)

with col2:

    st.pyplot(fig)



